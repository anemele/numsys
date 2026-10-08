use argh::FromArgs;
use numsys::NumSys;
use std::fs;
use std::io;
use std::io::BufRead;
use std::io::BufReader;

#[derive(Debug, FromArgs)]
/// numeral system: convert number between different bases.
struct Args {
    #[argh(option, short = 't', default = "16")]
    /// to base, default 16
    to_base: usize,

    #[argh(option, short = 'f', default = "10")]
    /// from base, default 10
    from_base: usize,

    #[argh(option, short = 'c')]
    /// charset, default [0-9A-Z]
    charset: Option<String>,

    #[argh(positional)]
    /// if not provided, read from stdin
    file: Option<String>,
}

fn read_file(path: Option<&str>) -> Box<dyn BufRead> {
    if let Some(p) = path {
        if let Ok(f) = fs::File::open(p) {
            return Box::new(BufReader::new(f));
        } else {
            eprintln!("cannot open file: {p}\nread from stdin")
        }
    }
    Box::new(io::stdin().lock())
}

fn main() {
    let args: Args = argh::from_env();

    let ns = match args.charset {
        None => NumSys::default(),
        Some(s) => match NumSys::new(&s) {
            Ok(ns) => ns,
            Err(e) => {
                eprintln!("{}", e);
                return;
            }
        },
    };
    if let Err(e) = ns.check_base(args.from_base, args.to_base) {
        eprintln!("{}", e);
        return;
    }

    read_file(args.file.as_deref())
        .lines()
        .map_while(Result::ok)
        .for_each(
            |line| match ns._convert(line.trim(), args.from_base, args.to_base) {
                Ok(s) => println!("{}", s),
                Err(e) => {
                    eprintln!("error: {}", e);
                    println!()
                }
            },
        );
}
