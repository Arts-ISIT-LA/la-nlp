## `[0.4.2]` -- 2023-02-28

### Fixed

- Fixed bug which allowed a token to be assigned a parent span that excluded the token itself.


## `[0.4.1]` -- 2023-02-21

### Changed

- [`get_token_parent_span()`](../la_nlp/components.py#L64) function now excludes children with dependency tags 'cc' and 'conj' from parent spans. These tags are generally used by the dependency parser when linking two separate clauses in the same sentence and therefore mark the border between semantically distinct sections. This change allows for more accurate parent span assignment and thus aspect sentiment evaluation when working with sentences following the pattern "I do A, but don't B".