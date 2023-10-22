@if exp="typeof(global.snow_object) == 'undefined'"
@iscript

/*
	ѩ��դ餻��ץ饰����
*/

class SnowGrain
{
	// ѩ���Υ��饹

	var fore; // �����ѩ�����֥�������
	var back; // �Y�����ѩ�����֥�������
	var xvelo; // ���ٶ�
	var yvelo; // �k�ٶ�
	var xaccel; // �����
	var l, t; // ��λ�äȿkλ��
	var ownwer; // ���Υ��֥������Ȥ����Ф��� SnowPlugin ���֥�������
	var spawned = false; // ѩ�������F���Ƥ��뤫
	var window; // ������ɥ����֥������Ȥؤβ���

	function SnowGrain(window, n, owner)
	{
		// SnowGrain ���󥹥ȥ饯��
		this.owner = owner;
		this.window = window;

		fore = new Layer(window, window.fore.base);
		back = new Layer(window, window.back.base);

		fore.absolute = 2000000-1; // �ؤͺϤ碌���ϥ�å��`���Ěs�����
		back.absolute = fore.absolute;

		fore.hitType = htMask;
		fore.hitThreshold = 256; // �ޥ�����å��`����ȫ��͸�^
		back.hitType = htMask;
		back.hitThreshold = 256;

		fore.loadImages("snow_" + n); // ������i���z��
		back.assignImages(fore);
		fore.setSizeToImageSize(); // �쥤��Υ���������Υ�������ͬ����
		back.setSizeToImageSize();
		xvelo = 0; // �᷽���ٶ�
		yvelo = n*0.6 + 1.9 + Math.random() * 0.2; // �k�����ٶ�
		xaccel = Math.random(); // ���ڼ��ٶ�
	}

	function finalize()
	{
		invalidate fore;
		invalidate back;
	}

	function spawn()
	{
		// ���F
		l = Math.random() * window.primaryLayer.width; // �����λ��
		t = -fore.height; // �k����λ��
		spawned = true;
		fore.setPos(l, t);
		back.setPos(l, t); // �Y�����λ�ä�ͬ����
		fore.visible = owner.foreVisible;
		back.visible = owner.backVisible;
	}

	function resetVisibleState()
	{
		// ��ʾ?�Ǳ�ʾ��״�B�����O������
		if(spawned)
		{
			fore.visible = owner.foreVisible;
			back.visible = owner.backVisible;
		}
		else
		{
			fore.visible = false;
			back.visible = false;
		}
	}

	function move()
	{
		// ѩ����Ӥ���
		if(!spawned)
		{
			// ���F���Ƥ��ʤ��Τǳ��F����C��򤦤�����
			if(Math.random() < 0.002) spawn();
		}
		else
		{
			l += xvelo;
			t += yvelo;
			xvelo += xaccel;
			xaccel += (Math.random() - 0.5) * 0.3;
			if(xvelo>=1.5) xvelo=1.5;
			if(xvelo<=-1.5) xvelo=-1.5;
			if(xaccel>=0.2) xaccel=0.2;
			if(xaccel<=-0.2) xaccel=-0.2;
			if(t >= window.primaryLayer.height)
			{
				t = -fore.height;
				l = Math.random() * window.primaryLayer.width;
			}
			fore.setPos(l, t);
			back.setPos(l, t); // �Y�����λ�ä�ͬ����
		}
	}

	function exchangeForeBack()
	{
		// ����Y�ι������򽻓Q����
		var tmp = fore;
		fore = back;
		back = tmp;
	}
}

class SnowPlugin extends KAGPlugin
{
	// ѩ����餹�ץ饰���󥯥饹

	var snows = []; // ѩ��
	var timer; // ������
	var window; // ������ɥ��ؤβ���
	var foreVisible = true; // ���椬��ʾ״�B���ɤ���
	var backVisible = true; // �Y���椬��ʾ״�B���ɤ���

	function SnowPlugin(window)
	{
		super.KAGPlugin();
		this.window = window;
	}

	function finalize()
	{
		// finalize �᥽�å�
		// ���Υ��饹�ι����뤹�٤ƤΥ��֥������Ȥ���ʾ�Ĥ��Ɨ�
		for(var i = 0; i < snows.count; i++)
			invalidate snows[i];
		invalidate snows;

		invalidate timer if timer !== void;

		super.finalize(...);
	}

	function init(num, options)
	{
		// num ����ѩ������F������
		if(timer !== void) return; // ���Ǥ�ѩ���ϤǤƤ���

		// ѩ��������
		for(var i = 0; i < num; i++)
		{
			var n = intrandom(0, 4); // ѩ���δ󤭤� ( ������ )
			snows[i] = new SnowGrain(window, n, this);
		}
		snows[0].spawn(); // �����ѩ����������������ʾ

		// �����ީ`������
		timer = new Timer(onTimer, '');
		timer.interval = 80;
		timer.enabled = true;

		foreVisible = true;
		backVisible = true;
		setOptions(options); // ���ץ������O��
	}

	function uninit()
	{
		// ѩ��������
		if(timer === void) return; // ѩ���ϤǤƤ��ʤ�

		for(var i = 0; i < snows.count; i++)
			invalidate snows[i];
		snows.count = 0;

		invalidate timer;
		timer = void;
	}

	function setOptions(elm)
	{
		// ���ץ������O������
		foreVisible = +elm.forevisible if elm.forevisible !== void;
		backVisible = +elm.backvisible if elm.backvisible !== void;
		resetVisibleState();
	}

	function onTimer()
	{
		// �����ީ`�����ڤ��Ȥ˺��Ф��
		var snowcount = snows.count;
		for(var i = 0; i < snowcount; i++)
			snows[i].move(); // move �᥽�åɤ���ӳ���
	}

	function resetVisibleState()
	{
		// ���٤Ƥ�ѩ���� ��ʾ?�Ǳ�ʾ��״�B�����O������
		var snowcount = snows.count;
		for(var i = 0; i < snowcount; i++)
			snows[i].resetVisibleState(); // resetVisibleState �᥽�åɤ���ӳ���
	}

	function onStore(f, elm)
	{
		// �ݤ򱣴椹��Ȥ�
		var dic = f.snows = %[];
		dic.init = timer !== void;
		dic.foreVisible = foreVisible;
		dic.backVisible = backVisible;
		dic.snowCount = snows.count;
	}

	function onRestore(f, clear, elm)
	{
		// �ݤ��i�߳����Ȥ�
		var dic = f.snows;
		if(dic === void || !+dic.init)
		{
			// ѩ�ϤǤƤ��ʤ�
			uninit();
		}
		else if(dic !== void && +dic.init)
		{
			// ѩ�ϤǤƤ���
			init(dic.snowCount, %[ forevisible : dic.foreVisible, backvisible : dic.backVisible ] );
		}
	}

	function onStableStateChanged(stable)
	{
	}

	function onMessageHiddenStateChanged(hidden)
	{
	}

	function onCopyLayer(toback)
	{
		// �쥤��α�����Y���Υ��ԩ`
		// ���Υץ饰����Ǥϥ��ԩ`���٤����ϱ�ʾ?�Ǳ�ʾ��������
		if(toback)
		{
			// ����Y
			backVisible = foreVisible;
		}
		else
		{
			// �Y����
			foreVisible = backVisible;
		}
		resetVisibleState();
	}

	function onExchangeForeBack()
	{
		// �Y�ȱ�ι������򽻓Q
		var snowcount = snows.count;
		for(var i = 0; i < snowcount; i++)
			snows[i].exchangeForeBack(); // exchangeForeBack �᥽�åɤ���ӳ���
	}
}

kag.addPlugin(global.snow_object = new SnowPlugin(kag));
	// �ץ饰���󥪥֥������Ȥ����ɤ������h����

@endscript
@endif
; �ޥ�����h
@macro name="snowinit"
@eval exp="snow_object.init(17, mp)"
@endmacro
@macro name="snowuninit"
@eval exp="snow_object.uninit()"
@endmacro
@macro name="snowopt"
@eval exp="snow_object.setOptions(mp)"
@endmacro
@return

