use std::mem::size_of;

use aes::{
    cipher::{generic_array::GenericArray, BlockEncrypt, KeyInit},
    Aes256Enc,
};
use clap::Parser;
use linux_syscall::{syscall, Result, Syscall};
use sha2::{Digest, Sha256};

#[allow(non_upper_case_globals)]
const SYS_get_flag: Syscall = Syscall::from_u32(548);

#[allow(non_upper_case_globals)]
const SYS_protect_flag: Syscall = Syscall::from_u32(549);

#[allow(non_upper_case_globals)]
const SYS_get_secret: Syscall = Syscall::from_u32(550);

fn read_secret_with_salt(idx: u32, salt: u32) -> u32 {
    let mut res = salt;

    let err = unsafe { syscall!(SYS_get_secret, idx, &mut res as *mut u32) };
    err.check().expect("get_secret fails");

    res
}

const S_LEN: usize = 32;

fn read_secrets_with_salts(data: &mut [u8; S_LEN], salts: &[u8; S_LEN]) {
    for idx in 0..S_LEN / 4 {
        let st = idx * 4;
        let salt = u32::from_ne_bytes(salts[st..st + 4].try_into().unwrap());

        let res = read_secret_with_salt(idx.try_into().unwrap(), salt);
        data[st..st + 4].copy_from_slice(&res.to_ne_bytes());
    }
}

fn sha256(data: &[u8; S_LEN]) -> [u8; S_LEN] {
    let mut hasher = Sha256::new();
    hasher.update(data);
    hasher.finalize().into()
}

const AES_KEY: [u8; S_LEN] = [
    209, 46, 72, 104, 110, 0, 48, 86, 165, 34, 203, 243, 181, 29, 109, 80, 205, 180, 129, 156, 218,
    80, 155, 175, 117, 204, 162, 69, 158, 195, 120, 196,
];

fn aes256(data: &[u8; S_LEN]) -> [u8; S_LEN] {
    let cipher = Aes256Enc::new_from_slice(&AES_KEY).unwrap();

    let mut res = [0; S_LEN];
    for idx in 0..S_LEN / 16 {
        let st = idx * 16;

        let blk_in = GenericArray::from_slice(&data[st..st + 16]);
        let mut blk_out = GenericArray::from_mut_slice(&mut res[st..st + 16]);
        cipher.encrypt_block_b2b(&blk_in, &mut blk_out);
    }

    res
}

fn compute_protect_key(secrets: &[u8; S_LEN]) -> usize {
    let mut res = 0;

    for st in (0..S_LEN).step_by(size_of::<usize>()) {
        res ^= usize::from_ne_bytes(secrets[st..st + size_of::<usize>()].try_into().unwrap());
    }

    res
}

fn protect_flag(idx: u32, key: usize) {
    let err = unsafe { syscall!(SYS_protect_flag, idx, key) };
    err.check().expect("protect_flag fails");
}

const MAX_FLAG_LEN: usize = 127;

fn read_flag(idx: u32, key: usize) -> String {
    let mut buf = [0u8; MAX_FLAG_LEN + 1];

    let err = unsafe { syscall!(SYS_get_flag, idx, &mut buf as *mut u8, key) };
    err.check().expect("get_flag fails");

    let flag = buf.into_iter().take_while(|c| *c != 0).collect();
    String::from_utf8(flag).unwrap()
}

#[derive(Parser)]
/// Where are my flags? This tool may be able to find one for me.
struct Cli {
    #[arg(short)]
    /// Well, I do NOT want to have a flag!
    protect: bool,

    #[arg(short, action = clap::ArgAction::Count)]
    /// Trust me bro, this option has NOTHING to do with the flags.
    show: u8,
}

const INITIAL_SALTS: [u8; S_LEN] = [
    93, 49, 51, 227, 153, 167, 160, 25, 210, 79, 118, 240, 200, 143, 97, 209, 70, 188, 202, 243,
    48, 26, 213, 178, 139, 28, 71, 107, 149, 213, 151, 206,
];

const TARGET_FLAG: u32 = 1;

fn main() {
    let cli = Cli::parse();

    let mut data = [0; S_LEN];
    read_secrets_with_salts(&mut data, &INITIAL_SALTS);

    let new_salts = sha256(&data);
    read_secrets_with_salts(&mut data, &new_salts);

    let new_salts = aes256(&data);
    read_secrets_with_salts(&mut data, &new_salts);

    let prot_key = compute_protect_key(&data);

    if cli.show == 7 {
        println!("Is this your flag? {}", prot_key);
    }

    if cli.protect {
        protect_flag(TARGET_FLAG, prot_key);
    } else {
        println!(
            "No luck, {}! Try to specify a different command.",
            read_flag(TARGET_FLAG, prot_key)
        );
    }
}
