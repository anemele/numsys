use std::{collections::HashMap, hash::Hash, str::FromStr};

#[derive(Debug, PartialEq)]
pub struct SeqMap<T>
where
    T: Eq + Hash + Clone,
{
    seq: Vec<T>,
    map: HashMap<T, usize>,
}

#[derive(Debug, PartialEq, thiserror::Error)]
pub enum SeqMapError {
    #[error("empty sequence")]
    Empty,
    #[error("duplicate character")]
    Duplicate,
}

#[allow(dead_code)]
impl<T> SeqMap<T>
where
    T: Eq + Hash + Clone,
{
    pub fn new(items: Vec<T>) -> Result<Self, SeqMapError> {
        if items.is_empty() {
            return Err(SeqMapError::Empty);
        }

        let mut seq = Vec::<T>::new();
        let mut map = HashMap::<T, usize>::new();
        for (i, it) in items.into_iter().enumerate() {
            if map.contains_key(&it) {
                return Err(SeqMapError::Duplicate);
            }
            map.insert(it.clone(), i);
            seq.push(it);
        }
        Ok(Self { seq, map })
    }

    pub fn get_index(&self, key: &T) -> Option<usize> {
        self.map.get(key).copied()
    }

    pub fn get_by_index(&self, idx: usize) -> Option<&T> {
        self.seq.get(idx)
    }

    pub fn len(&self) -> usize {
        self.seq.len()
    }

    pub fn is_empty(&self) -> bool {
        // requires non-empty vector
        false
    }

    pub fn iter(&self) -> std::slice::Iter<'_, T> {
        self.seq.iter()
    }

    pub fn as_vec(&self) -> &Vec<T> {
        self.seq.as_ref()
    }
}

impl TryFrom<&str> for SeqMap<char> {
    type Error = SeqMapError;

    fn try_from(s: &str) -> Result<Self, Self::Error> {
        Self::new(s.chars().collect())
    }
}

impl FromStr for SeqMap<char> {
    type Err = SeqMapError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::try_from(s)
    }
}

impl<T> TryFrom<&[T]> for SeqMap<T>
where
    T: Eq + Hash + Clone,
{
    type Error = SeqMapError;

    fn try_from(value: &[T]) -> Result<Self, Self::Error> {
        Self::new(value.to_vec())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_seqmap() {
        let char_set = "abcde";
        let seqmap = SeqMap::try_from(char_set).unwrap();
        assert_eq!(seqmap.get_index(&'a'), Some(0));
        assert_eq!(seqmap.get_index(&'b'), Some(1));
        assert_eq!(seqmap.get_index(&'c'), Some(2));
        assert_eq!(seqmap.get_index(&'d'), Some(3));
        assert_eq!(seqmap.get_index(&'e'), Some(4));
        assert_eq!(seqmap.get_index(&'f'), None);
        assert_eq!(seqmap.get_by_index(0), Some(&'a'));
        assert_eq!(seqmap.get_by_index(1), Some(&'b'));
        assert_eq!(seqmap.get_by_index(2), Some(&'c'));
        assert_eq!(seqmap.get_by_index(3), Some(&'d'));
        assert_eq!(seqmap.get_by_index(4), Some(&'e'));
        assert_eq!(seqmap.get_by_index(5), None);
        assert_eq!(seqmap.len(), 5);
        assert!(!seqmap.is_empty());
    }

    #[test]
    fn test_seqmap_error() {
        assert_eq!(SeqMap::try_from(""), Err(SeqMapError::Empty));
        assert_eq!(SeqMap::try_from("abca"), Err(SeqMapError::Duplicate));
    }
}
