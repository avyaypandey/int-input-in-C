/// Reads an integer from stdin into a preallocated C buffer.
///
/// # Purpose
/// Provides a safe, Rust-backed input function for C programs, avoiding
/// undefined behavior and memory leaks from manual allocation.
///
/// # Parameters
/// - `prompt`: A C string to display to the user. If `NULL`, defaults to `"Enter a number: "`.
/// - `buf`: A mutable buffer provided by the C caller. The input number (as string) will
///          be written here, null-terminated.
/// - `buf_len`: Length of the buffer in bytes. Must be >= 1.
///
/// # Returns
/// - `0` on success (buffer now contains a valid integer string).
/// - `1` on any error:
///   - `buf` is null or zero length
///   - I/O error
///   - empty input
///   - non-digit characters in input
///
/// # Notes / Quirks
/// - This function **does not allocate memory**; the caller owns the buffer.
/// - Any invalid input is reported via `stderr` and returns `1` immediately.
/// - Only **positive integers** are accepted; negative signs or other characters fail.
/// - Uses `unsafe` to convert raw pointers; the caller must ensure valid pointers.


use std::ffi::CStr; 
use std::os::raw::c_char;
use std::io::{self, Write};
use std::slice;

#[unsafe(no_mangle)]
pub extern "C" fn read_int_into_buffer(prompt: *const c_char, buf: *mut c_char, buf_len: usize) -> i32 {
    if buf.is_null() || buf_len == 0 {
        eprintln!("Wrong buffer provided");
        return 1;
    }

    let prompt_str_u = unsafe {
        if prompt.is_null(){
            "Enter a number: "
        } else {
            CStr::from_ptr(prompt)
                .to_str()
                .unwrap_or("Enter a number: ")
        }
    };

    let mut input_num = String::new();
    
    print!("{}", prompt_str_u);
    io::stdout().flush().unwrap();

    if io::stdin().read_line(&mut input_num).is_err() {
        eprintln!("\nError in I/O");
        return 1;
    }

    let input_num = input_num.trim();

    if input_num.is_empty() {
        eprintln!("\nEmpty input");
        return 1;
    }

    if !input_num.chars().all(|c| c.is_ascii_digit()) {
        eprintln!("\nEnter a valid number");
        return 1;
    }

    // Convert to i32 and check for overflow when multiplied by 10
    let number: i32 = match input_num.parse() {
        Ok(n) => n,
        Err(_) => {
            eprintln!("\nNumber too large");
            return 1;
        }
    };

    if number > i32::MAX / 10 {
        eprintln!("\nNumber too large: would overflow when multiplied by 10");
        return 1;
    }

    let bytes = input_num.as_bytes();
    let len = bytes.len().min(buf_len-1);
    unsafe {
        let dst = slice::from_raw_parts_mut(buf as *mut u8, buf_len);
        dst[..len].copy_from_slice(&bytes[..len]);
        dst[len] = 0;
    }

    0
}

