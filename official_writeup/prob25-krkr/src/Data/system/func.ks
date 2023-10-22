;------------------------------------------------------------
;   KAGeXpress ver 3.0 ��װ�꼯
;   Author: Miliardo/2006.11.5
;   Author: ��ɽ��ҹ/Ver 2.0
;
;   http://kcddp.keyfc.net/
;   (C) 2002-2006��Key Fans Club
;
;------------------------------------------------------------


;------------------------------------------------------------
;    ��ʼ�趨
;------------------------------------------------------------

*init

@loadplugin module=wuvorbis.dll
@loadplugin module=wump3.dll
@loadplugin module=wutcwf.dll
@loadplugin module=extrans.dll
@loadplugin module=extNagano.dll

@if exp="global.useconfigMappfont==true"
@mappfont storage=&global.configMappfont
@endif

@macro name=vend
@if exp="tf.KAGeXpress_voice=1"
@eval exp="tf.KAGeXpress_voice=0"
@endhact
@endif
@endmacro

@macro name=p
@vend
@oporig
@endmacro

@call storage=snow.ks
@call storage=rain.ks
@call storage=staffroll.ks

;�����ط��õ�Buffer
@iscript
tf.WSB=new WaveSoundBuffer(null);
tf.strs1="histvoice(\"";
tf.strs2="\")";
tf.KAGeXpress_voice=0;
function histvoice(storage)
{
	kag.se[0].stop();
	if(!Storages.isExistentStorage(storage))
	{
		var test;
		if(test = storage + ".wav", Storages.isExistentStorage(test))
			storage = test;
		else if(test = storage + ".ogg", Storages.isExistentStorage(test))
			storage = test;
		else if(test = storage + ".tcw", Storages.isExistentStorage(test))
			storage = test;
		else if(test = storage + ".mp3", Storages.isExistentStorage(test))
			storage = test;
		else
			throw new Exception("���� " + storage + " δ�ҵ�");
	}
	tf.WSB.open(storage);
	tf.WSB.play();
}
@endscript


;------------------------------------------------------------
;    ���ݵ���
;------------------------------------------------------------
;ǰ��ͼ�������޸ģ�Ĭ��Ϊ3����
@autolabelmode mode=true
@erafterpage mode=true

;------------------------------------------------------------
;    Macro���򣨿ɸ���������е�����
;------------------------------------------------------------

;���ﵭ����ʾ
;fg us rule=xxx ....��ִ��Universal Transition
@macro name=fg
@eval exp="mp.method=universal" cond=mp.us
@backlay
@image * layer=%layer|%lay|0 page=back storage=%storage|%file visible=true key=%key left=%l top=%t opacity=%op pos=%pos
@trans * method=%method|crossfade time=%time|200 layer=base
@wt
@endmacro

;������(layerΪ������)/���һ��(cl all)
;������keep=msg/keep=back
;fg us rule=xxx ....��ִ��Universal Transition
@macro name=cl
@eval exp="mp.method=universal" cond=mp.us
@if exp=mp.all
@clearlayers page=back
@backlay layer=message cond=mp.keep=="msg"|"back"
@backlay layer=base cond=mp.keep=="back"
@clearlayers page=fore keep=%keep
@copylay srclayer=message destlayer=message srcpage=back destpage=fore cond=mp.keep=="msg"|"back"
@copylay srclayer=message destlayer=message srcpage=back destpage=fore cond=mp.keep=="back"
@endif
@backlay
@freeimage layer=%layer|%lay|0 page=back
@trans * method=%method|crossfade time=%time|200 layer=base
@wt
@endmacro

;�����л�/���뵭��
;fg us rule=xxx ....��ִ��Universal Transition
@macro name=bg
@eval exp="mp.method=universal" cond=mp.us
@backlay
@image * layer=base storage=%storage|%file layer=base page=back left=%l top=%t
@trans * method=%method|crossfade time=%time|0 layer=base
@wt
@endmacro

;���ֵ������
@macro name=lr
@l
@r
@endmacro

;���ֲ���/ֹͣ���ֲ���
@macro name=bgm
@if exp=mp.play||(!mp.stop)
@if exp=mp.time!=0
@xchgbgm storage=%storage|%file overlap=%time loop=%loop|true volume=%volume|100
@endif
@if exp=mp.time==(void)
@playbgm storage=%storage|%file loop=%loop|true volume=%volume|100
@endif
@endif
@if exp=mp.stop
@fadeoutbgm buf=%buf|0 time=%time|0
@endif
@if exp=mp.wait
@wb buf=%buf|0
@endif
@endmacro

;��Ч����/ֹͣ��Ч����
@macro name=se
@if exp=mp.play||(!mp.stop)
@if exp=mp.time!=0
@fadeinse buf=%buf|0 storage=%storage|%file time=%time volume=%volume|100 loop=%loop|false loop=%loop|false
@endif
@if exp=mp.time==(void)
@playse storage=%storage|%file loop=%loop|false volume=%volume|100 buf=%buf|0
@endif
@endif
@if exp=mp.stop
@fadeoutse buf=0 time=%time|0
@endif
@if exp=mp.wait
@wf buf=%buf|0
@ws buf=%buf|0
@endif
@endmacro

;��������(���Իط�)
@macro name=vo
@if exp=mp.play||(!mp.stop)
@eval exp="tf.WSB.stop()"
@eval exp="tf.KAGeXpress_voice=1"
@playse storage=%storage|%file buf=1
@eval exp="tf.ds=tf.strs1+mp.file+tf.strs2"
@hact exp=&tf.ds
@endif
@if exp=mp.stop
@stopse buf=1
@endif
@endmacro

;��Ƶ����
@macro name=movie
@video visible=true left=0 top=0 width=640 height=480
@playvideo storage=%storage|%file
@wv canskip=true
@endmacro

;�ȴ���Ч���Ž���
@macro name=wse
@ws buf=1 canskip=true
@endmacro

;�ȴ��������Ž���
@macro name=wvo
@ws buf=0 canskip=true
@endmacro

;���ֲ����Ե���
@macro name=frame
[position layer=%layer|%layer|message0 page=fore visible=true opacity=%op top=%t height=%h left=%l width=%w marginl=%ml margint=%mt marginr=%mr marginb=%mb frame=%frame| ]
@endmacro

;����/��ѩ/��Ч��
@macro name=fx

@if exp=mp.rain
@if exp=!mp.stop
@raininit forevisible=true backvisible=true
@playse storage=rain.wav buf=2 loop=true
@endif
@if exp=mp.stop
@rainuninit
@stopse buf=2
@endif
@endif

@if exp=mp.snow
@if exp=!mp.stop
@snowinit forevisible=true backvisible=true
@endif
@if exp=mp.stop
@snowuninit
@stopse buf=2
@endif

@endif

@if exp=mp.shake
@quake time=%time hmax=%h vamx=%v
@if exp=mp.wait==true
@wq
@endif
@endif

@endmacro

;������
@macro name=shake
@quake time=%time hmax=%h vamx=%v
@endmacro

;���ֿ���ʾ/��ʧ
@macro name=text

@if exp=mp.on
@backlay
@layopt layer=message page=back visible=true
@trans method=crossfade time=%time|0
@wt
@layopt layer=message page=fore visible=true
@endif

@if exp=mp.off
@layopt layer=message page=back visible=false
@trans method=crossfade time=%time|0
@wt
@layopt layer=message page=fore visible=false
@endif

@endmacro
@call storage=textset.ks
;------------------------------------------------------------
;    Macro����
;------------------------------------------------------------
@jump storage=first.ks

