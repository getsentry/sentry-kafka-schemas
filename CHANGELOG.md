# Changelog and versioning

## 0.0.11

### Various fixes & improvements

- fix: Do not attempt to push formatting changes into release branch (#54) by @untitaker
- feat(metric alerts): Add schema, topic, and example (#49) by @ceorourke
- ref: Add autoformatting for JSON (#51) by @untitaker

## 0.0.10

### Various fixes & improvements

- feat(querylog): Improve schema (#53) by @lynnagara
- build: pyyaml>=5.4,<7.0 (#52) by @lynnagara
- doc: Add info on how to add a docstring to types (#50) by @untitaker
- fix: Accept client_ip in sdk_info (#48) by @untitaker
- ref: Bump jsonschema-gentypes (#47) by @untitaker
- doc: Add information about releasing this package (#46) by @untitaker
- feat: Add rapidjson to testmatrix (#44) by @untitaker

## 0.0.9

### Various fixes & improvements

- feat: Add threads to events schema (#45) by @marandaneto

## 0.0.8

### Various fixes & improvements

- fix(tests): Broken Organization ID test (#43) by @rahul-kumar-saini
- fix(slo) Add the request_status / slo fields to the top level (#42) by @evanh
- feat(Querylog): Organization ID Field (#41) by @rahul-kumar-saini
- fix: Relax TransactionSource definition (#40) by @untitaker

## 0.0.7

### Various fixes & improvements

- feat: Generate type for where profile (#39) by @lynnagara
- feat: Add basic linting for jsonschema naming conventions (#36) by @untitaker
- fix: Split out linting for Rust (#38) by @untitaker
- fix: Another instance of nullable tags (#37) by @untitaker

## 0.0.6

### Various fixes & improvements

- fix(querylog) Add SLO related fields to the schema (#35) by @evanh

## 0.0.5

### Various fixes & improvements

- feat: Add basic iter_examples function (#33) by @untitaker
- fix: Enforce minimum required on typing-extensions (#34) by @untitaker
- fix(eventstream): Add all other message types (#32) by @untitaker
- fix: Fix event schema wrt nullable tag keys (#31) by @untitaker
- fix: Add more typing docs (#30) by @untitaker

## 0.0.4

### Various fixes & improvements

- ref: Bump jsonschema-gentypes to fork (#29) by @untitaker

## 0.0.3

### Various fixes & improvements

- fix(ci): Bump timeout of linter job (#28) by @untitaker
- fix: Relax result_profile in querylog schema (#27) by @untitaker
- feat: Implement `get_schema` in Rust (#26) by @lynnagara
- test: Add more topic validation (#25) by @lynnagara
- ref: Add Python types (#24) by @untitaker
- feat: Add topic description (#23) by @lynnagara
- fix: Fix all topic names (#22) by @lynnagara
- test: Add check for topic name validity (#21) by @lynnagara

## 0.0.2

### Various fixes & improvements

- fix: Rename "errors topic" to its actual name in prod (#20) by @untitaker
- feat(querylog): Stricter schema (#18) by @lynnagara
- build: Add py.typed for mypy type annotations (#17) by @lynnagara
- fix: Fix all known event schema errors (#19) by @untitaker
- ref: Add schemas and more CI (#16) by @untitaker
- feat(python): Respect the version number requested (#15) by @lynnagara
- test: Add test that loads all topics (#14) by @lynnagara
- feat: Add Rust library (#13) by @lynnagara

## 0.0.1

- First release 🎉
