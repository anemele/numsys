use crate::seqmap::{SeqMap, SeqMapError};
use num_bigint::BigUint;
use num_traits::ToPrimitive;

// pub const DEFAULT_CHARSET: &str = "0123456789abcdefghijklmnopqrstuvwxyz";
const DEFAULT_CHARSET: &str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const MINUMUM_BASE: usize = 2;

pub struct NumSys {
    seqmap: SeqMap<char>,
}

#[derive(Debug, PartialEq, thiserror::Error)]
pub enum NumSysError {
    #[error("init failed: {0}")]
    Init(#[from] SeqMapError),

    #[error("not found char `{0}`")]
    NotFoundChar(char),

    #[error("base > MAX({0})")]
    BaseGTM(usize),

    #[error("base < 2")]
    BaseLT2,
}

type RResult<T> = Result<T, NumSysError>;

impl NumSys {
    pub fn new(s: &str) -> RResult<Self> {
        let seqmap = SeqMap::try_from(s)?;
        Ok(Self { seqmap })
    }

    fn convert_to_decimal(&self, num: &str, base: usize) -> RResult<BigUint> {
        let mut decimal = BigUint::ZERO;
        for c in num.chars() {
            let digit_val = self
                .seqmap
                .get_index(&c)
                .ok_or(NumSysError::NotFoundChar(c))?;
            if digit_val >= base {
                return Err(NumSysError::BaseGTM(base));
            }
            decimal = decimal * base + digit_val;
        }

        Ok(decimal)
    }

    fn convert_to_str(&self, decimal: BigUint, base: usize) -> RResult<String> {
        if decimal == BigUint::ZERO {
            return Ok(self
                .seqmap
                .get_by_index(0)
                // length > 0, unwrap is ok
                .unwrap()
                .to_string());
        }

        let mut num = String::new();
        let mut remainder = decimal;
        let big_base = BigUint::from(base);

        while remainder >= big_base {
            let idx = (&remainder % base).to_usize().unwrap();
            let nn = self.seqmap.get_by_index(idx).unwrap();
            num.push(*nn);
            remainder /= base;
        }
        if remainder > BigUint::ZERO {
            let nn = self
                .seqmap
                .get_by_index(remainder.to_usize().unwrap())
                .unwrap();
            num.push(*nn);
        }
        let num = num.chars().rev().collect();

        Ok(num)
    }

    /// NOTE: only used for checked base
    pub fn _convert(&self, num: &str, from_base: usize, to_base: usize) -> RResult<String> {
        let decimal = self.convert_to_decimal(num, from_base)?;
        let num = self.convert_to_str(decimal, to_base)?;
        Ok(num)
    }

    pub fn check_base(&self, from_base: usize, to_base: usize) -> RResult<()> {
        let len = self.seqmap.len();
        if from_base < MINUMUM_BASE || to_base < MINUMUM_BASE {
            Err(NumSysError::BaseLT2)
        } else if from_base > len || to_base > len {
            Err(NumSysError::BaseGTM(len))
        } else {
            Ok(())
        }
    }

    pub fn convert(&self, num: &str, from_base: usize, to_base: usize) -> RResult<String> {
        self.check_base(from_base, to_base)?;

        if from_base == to_base {
            return Ok(num.to_string());
        }

        self._convert(num, from_base, to_base)
    }
}

/// TODO: default impl use [0-9A-Z]
/// for base 2, 8, 16 may have more optimized method
/// BigUint also supports
/// {:b} {:o} {:x} {:X}
impl Default for NumSys {
    fn default() -> Self {
        Self {
            // unwrap is ok
            seqmap: SeqMap::try_from(DEFAULT_CHARSET).unwrap(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_numsys() {
        let numsys = NumSys::default();
        assert_eq!(
            numsys.convert_to_decimal("1234", 10).unwrap(),
            1234u32.into()
        );
        assert_eq!(
            numsys.convert_to_decimal("101010", 2).unwrap(),
            42u32.into()
        );
        assert_eq!(
            numsys.convert_to_decimal("ABCD", 16).unwrap(),
            43981u32.into()
        );
    }

    #[test]
    fn test_invalid_digit() {
        let numsys = NumSys::default();
        assert!(numsys.convert_to_decimal("1234", 2).is_err());
        assert!(numsys.convert_to_decimal("101010", 1).is_err());
        assert!(numsys.convert_to_decimal("ABCD", 10).is_err());
    }

    #[test]
    fn test_convert_to_base() {
        let numsys = NumSys::default();
        assert_eq!(numsys.convert_to_str(1234u32.into(), 10).unwrap(), "1234");
        assert_eq!(numsys.convert_to_str(42u32.into(), 2).unwrap(), "101010");
        assert_eq!(numsys.convert_to_str(43981u32.into(), 16).unwrap(), "ABCD");
    }

    #[test]
    fn test_convert_to_base_zero() {
        let numsys = NumSys::default();
        assert_eq!(numsys.convert_to_str(0u32.into(), 10).unwrap(), "0");
        assert_eq!(numsys.convert_to_str(0u32.into(), 2).unwrap(), "0");
        assert_eq!(numsys.convert_to_str(0u32.into(), 16).unwrap(), "0");
    }

    #[test]
    fn test_convert_to_base_large() {
        let numsys = NumSys::default();
        assert_eq!(
            numsys.convert_to_str(1234567890u32.into(), 10).unwrap(),
            "1234567890"
        );
    }

    #[test]
    fn test_convert() {
        let numsys = NumSys::default();
        assert_eq!(numsys.convert("1234", 10, 2).unwrap(), "10011010010");
        assert_eq!(numsys.convert("101010", 2, 10).unwrap(), "42");
        assert_eq!(numsys.convert("ABCD", 16, 10).unwrap(), "43981");
    }

    #[test]
    fn test_convert_invalid_digit() {
        let numsys = NumSys::default();
        assert!(numsys.convert("1234", 2, 10).is_err());
        assert!(numsys.convert("101010", 1, 10).is_err());
        assert!(numsys.convert("ABCD", 10, 16).is_err());
    }

    #[test]
    fn test_convert_same_base() {
        let numsys = NumSys::new("ABCD").unwrap();
        assert_eq!(numsys.convert("A", 2, 4).unwrap(), "A");
        assert_eq!(numsys.convert("B", 2, 4).unwrap(), "B");
        assert_eq!(numsys.convert("BA", 2, 4).unwrap(), "C");
        assert_eq!(numsys.convert("BB", 2, 4).unwrap(), "D");
    }
}
