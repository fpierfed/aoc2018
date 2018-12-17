use std::env;
use std::fs;
use std::process;


fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("usage: {} <input file>", args[0]);
        process::exit(1);
    }

    let filename = &args[1];
    let data = fs::read_to_string(filename)
        .expect("Unable to read input file");
    let data = data.trim().to_string();

    println!("{}", process(data).len());
}


fn process(data: String) -> String {
    // This takes COMPLETE ownership of the input string and returns a new one

    let mut start = 0;
    let mut data_length = data.len();
    let mut s = data.clone();

    loop {
        let (new_start, new_s) = _process(start, s);
        s = new_s;
        if s.len() == 0 {
            // We are done
            break s;
        } else if s.len() != data_length {
            // We found something: keep going
            data_length = s.len();
            start = new_start;
        } else {
            // The strings are the same: nothing else to do
            break s;
        }
    }
}


fn _process(start: usize, data: String) -> (usize, String) {
    // This takes COMPLETE ownership of its inputs

    let bdata = data.as_bytes();
    let mut i = start;
    while bdata.len() > 0 && i < bdata.len() - 1 {
        let first = bdata[i];
        let second = bdata[i + 1];

        if second != first && second.to_ascii_uppercase() == first.to_ascii_uppercase() {
            let new_data = data[..i].to_string() + &(data[i + 2..]);
            if i == 0 {
                return (i, new_data);
            } else {
                return (i - 1, new_data);
            }
        } else {
            i = i + 1;
        }
    }
    (start, data.to_string())
}
