#[derive(PartialEq, Debug)]
pub struct Schema {}

pub fn get_schema(topic: &str, version: Option<u16>) -> Option<Schema> {
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_schema() {
        assert_eq!(get_schema("asdf", None), None);
    }
}
