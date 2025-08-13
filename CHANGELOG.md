# Changelog and versioning

## 2.1.0

### Various fixes & improvements

- chore(span-buffer): Add downsampled_retention_days to the SegmentSpan schema (#432) by @phacops

## 2.0.4

- No documented changes.

## 2.0.2

### Various fixes & improvements

- Allow span link attributes to be null (#428) by @gggritso

## 2.0.1

### Various fixes & improvements

- feat: snuba-items items dlq topic definition (#427) by @kylemumma

## 2.0.0

### Various fixes & improvements

- chore: Delete unused topics (#426) by @phacops

## 1.3.18

### Various fixes & improvements

- feat(taskworker): Define default topic config for taskworker workflows engine dlq (#425) by @enochtangg
- feat(tasks): Add taskworker-workflows-events kafka topic (#424) by @kcons

## 1.3.17

### Various fixes & improvements

- Add definitions for span links (#422) by @gggritso

## 1.3.16

### Various fixes & improvements

- feat(tasks) Add taskworker-ingest-errors-postprocess topics (#423) by @markstory

## 1.3.15

### Various fixes & improvements

- ref(snuba-items): add LogAppendTime to snuba-items topic (#421) by @MeredithAnya

## 1.3.14

### Various fixes & improvements

- feat(taskworker) Add new topic for buffer tasks (#419) by @markstory

## 1.3.13

### Various fixes & improvements

- fix(uptime): Refine new fields on the `uptime-results` schema (#418) by @wedamija

## 1.3.12

### Various fixes & improvements

- feat(launchpad): Create new kafka schema for launchpad (#417) by @NicoHinderling

## 1.3.11

### Various fixes & improvements

- feat(uptime): Add optional fields to the `RequestInfo` schema to track more request detail (#416) by @wedamija

## 1.3.10

### Various fixes & improvements

- Add ingest-spans-dlq (#415) by @untitaker

## 1.3.9

### Various fixes & improvements

- create taskworker ingest and attachments topics (#414) by @enochtangg

## 1.3.8

### Various fixes & improvements

- Upgrade rapidjson (#413) by @fpacifici

## 1.3.7

### Various fixes & improvements

- feature(errors) - Add `sample_rate` field to ErrorData on error events (#412) by @yuvmen

## 1.3.6

### Various fixes & improvements

- fix: Add missing fields to buffered-segments and ingest-spans (#411) by @jan-auer

## 1.3.5

### Various fixes & improvements

- add taskworker email and cutover topics configs (#410) by @enochtangg

## 1.3.4

### Various fixes & improvements

- chore(eap): Add item subscription related topics (#409) by @phacops

## 1.3.3

### Various fixes & improvements

- fix: Sort slice by resource instead of topic (#408) by @phacops

## 1.3.2

### Various fixes & improvements

- fix(rust): Fix compilation with no default features enabled (#407) by @Dav1dde

## 1.3.1

### Various fixes & improvements

- chore: Update sentry-protos to 0.2.0 for real (#406) by @phacops

## 1.3.0

### Various fixes & improvements

- chore: Update sentry-protos to 0.2.0 (#405) by @phacops
- ref(taskworker): Add all the remaining topics needed for the taskworker (#404) by @evanh
- add ingest errors topic config (#403) by @enochtangg

## 1.2.2

### Various fixes & improvements

- chore: Update sentry-protos to 0.1.74 (#402) by @phacops

## 1.2.1

### Various fixes & improvements

- feat(taskworker): Add taskworker control and dlq topic configurations (#401) by @enochtangg
- feat(snuba-spans): add `kind` field (#400) by @mjq
- ref: bump sentry-protos to 0.1.69 (#399) by @phacops

## 1.2.0

### Various fixes & improvements

- ref(uptime): Remove uptime-configs topic (#398) by @evanpurkhiser

## 1.1.7

### Various fixes & improvements

- feat(eap): Add schema for snuba-items (#390) by @phacops

## 1.1.6

### Various fixes & improvements

- chore(sourcemaps) - Update ErrorDate kafka schema (#396) by @yuvmen
- remove old task-worker topic (#395) by @enochtangg

## 1.1.5

### Various fixes & improvements

- feat(taskworker): Add taskworker ingest and dlq topics (#394) by @enochtangg

## 1.1.4

### Various fixes & improvements

- chore(taskworker): Temporarily add task-worker (#393) by @enochtangg

## 1.1.3

### Various fixes & improvements

- fix(taskworker): Rename taskworker topic (#392) by @enochtangg

## 1.1.2

### Various fixes & improvements

- fix(spans): Align the spans topics with reality (#389) by @jan-auer

## 1.1.1

### Various fixes & improvements

- feat: Introduce ingest-spans (#388) by @jan-auer

## 1.1.0

### Various fixes & improvements

- feat(uptime): add redirect error (#387) by @JoshFerge

## 1.0.8

### Various fixes & improvements

- feat(uptime): Add additional "incident_status" to snuba results (#386) by @evanpurkhiser
- add more missing pipeline annotations (#385) by @lynnagara

## 1.0.7

### Various fixes & improvements

- fix incorrect pipeline annotations (#384) by @lynnagara
- fix(crons): Correct description of start_time (#383) by @evanpurkhiser

## 1.0.6

### Various fixes & improvements

- Creating the events backlog topic (#380) by @kneeyo1
- bump version (#382) by @kneeyo1

## 1.0.5

### Various fixes & improvements

- fix: bump sentry-protos (#381) by @JoshFerge

## 1.0.4

### Various fixes & improvements

- Revert "Add feature flag context (#364)" (#379) by @cmanallen

## 1.0.3

### Various fixes & improvements

- feat(uptime): add new failure types (#377) by @JoshFerge
- Improve support for protocol buffer topics in rust library (#370) by @markstory
- feat(uptime): add environment to snuba uptime results schema (#375) by @JoshFerge

## 1.0.2

### Various fixes & improvements

- add a `$bytes: true` schema extension and use it for monitor payload (#374) by @asottile-sentry

## 1.0.1

### Various fixes & improvements

- Revert "fill out type for MonitorCheckIn.payload (#372)" (#373) by @asottile-sentry

## 1.0.0

### Various fixes & improvements

- fill out type for MonitorCheckIn.payload (#372) by @asottile-sentry
- Add feature flag context (#364) by @cmanallen
- ref(uptime): remove region_slug from schema (#368) by @JoshFerge
- codeowners replay backend (#369) by @bruno-garcia

## 0.1.129

### Various fixes & improvements

- feat: add schemas for ourlogs (#367) by @colin-sentry

## 0.1.128

### Various fixes & improvements

- release: 0.1.127 (08569708) by @getsentry-bot

## 0.1.127

- No documented changes.

## 0.1.126

### Various fixes & improvements

- feat(uptime): Include region in uptime results (#363) by @wedamija

## 0.1.125

### Various fixes & improvements

- chore: Tidy up a few things related to file references (#362) by @wedamija
- feat(uptime): new snuba-uptime-results topic (#361) by @wedamija
- feat: Allow schemas to reference other schemas (#360) by @wedamija

## 0.1.124

### Various fixes & improvements

- chore(uptime): Improve generated schema for uptime region configs (#358) by @wedamija

## 0.1.123

### Various fixes & improvements

- feat(uptime): Add regions to uptime config (#357) by @wedamija

## 0.1.122

### Various fixes & improvements

- deprecate(hierarchical_hashes): Remove references to hierarchical hashes (#353) by @armenzg

## 0.1.121

### Various fixes & improvements

- chore(metrics-summaries): Remove metrics summaries related code (#352) by @phacops

## 0.1.120

### Various fixes & improvements

- feat(uptime): add trace_sampling to kafka schema (#351) by @JoshFerge

## 0.1.119

### Various fixes & improvements

- ref(crons): Remove volume_anomaly_result from mark_missing task (#350) by @evanpurkhiser
- ref(crons): Remove unused `volume_anomaly_result` from clock_tick (#349) by @evanpurkhiser

## 0.1.118

### Various fixes & improvements

- feat(crons): Add monitors-incident-occurrences (#348) by @evanpurkhiser

## 0.1.117

### Various fixes & improvements

- ref(deletes): search-issues -> generic-events (#347) by @MeredithAnya
- feat(protobuf) Add support for protobuf message topics (#344) by @markstory

## 0.1.116

### Various fixes & improvements

- feat: Add taskworker schema (#343) by @markstory

## 0.1.115

### Various fixes & improvements

- ref(snuba-bulk-deletes): add snuba-lw-deletions topic/schema (#338) by @MeredithAnya

## 0.1.114

### Various fixes & improvements

- feat(crons): Add mark_unknown clock task (#340) by @evanpurkhiser
- feat(crons): Add `volume_anomaly_result` to mark_missing task (#341) by @evanpurkhiser
- fix(crons): Switch to `enum` as a shape Discriminator in clock tasks (#342) by @evanpurkhiser
- feat(crons): Add "volume_anomaly_result" result to clock-tick (#339) by @evanpurkhiser

## 0.1.113

### Various fixes & improvements

- Add topic configurations required for EAP alerts (#337) by @shruthilayaj

## 0.1.112

### Various fixes & improvements

- c (#336) by @xurui-c

## 0.1.111

### Various fixes & improvements

- ref(uptime): Switch request_headers to a array of tuples (#334) by @evanpurkhiser

## 0.1.110

### Various fixes & improvements

- feat(eap): Add EAP mutations topic (#333) by @ayirr7

## 0.1.109

### Various fixes & improvements

- chore(github): Bump `upload-artifact` to v4 (#332) by @wedamija
- feat(uptime): Add request{method,headers,body} fields (#330) by @evanpurkhiser
- ref(uptime): Allow additional methods in `rquest_type` (#331) by @evanpurkhiser

## 0.1.107

### Various fixes & improvements

- build: Streamline dependencies (#329) by @jan-auer
- fix(uptime): Require span_id (#328) by @evanpurkhiser

## 0.1.106

### Various fixes & improvements

- ref(generic-metrics): Rename sample_weigth to sampling_weight (#327) by @john-z-yang

## 0.1.105

### Various fixes & improvements

- fix(generic-metrics): Use floating point as sample weight (#326) by @john-z-yang

## 0.1.104

### Various fixes & improvements

- add sampling to metrics schema (#325) by @john-z-yang
- Add start_timestamp_precise, end_timestamp_precise, and organization_id as required span attrs (#323) by @colin-sentry

## 0.1.103

### Various fixes & improvements

- fix(metrics_summaries): Accept metrics summaries with only count (#322) by @phacops

## 0.1.102

### Various fixes & improvements

- chore(billing): Add DLQ schemas (#321) by @dashed

## 0.1.101

### Various fixes & improvements

- ref(uptime): Add `_ms` suffix to timestamps (#320) by @evanpurkhiser

## 0.1.100

### Various fixes & improvements

- ensure dlq topics have the same message size as their underlying topics (#319) by @lynnagara
- Update name for field to match new column name (#318) by @snigdhas

## 0.1.99

### Various fixes & improvements

- fix(uptime): Fix required elements of schema to match properties (#317) by @wedamija

## 0.1.98

### Various fixes & improvements

- fix(uptime): Improve naming of interval = timeout (#316) by @evanpurkhiser

## 0.1.97

### Various fixes & improvements

- feat(uptime): Add uptime-results topic (#313) by @evanpurkhiser
- test: Allow -1 retention when cleanup.policy: compact (#314) by @evanpurkhiser

## 0.1.96

### Various fixes & improvements

- fix event-replacements topic (#312) by @lynnagara

## 0.1.95

### Various fixes & improvements

- Update first_release_id field to integer or null (#310) by @snigdhas
- add topic definition, schema and examples for ingest-transactions (#311) by @lynnagara

## 0.1.94

### Various fixes & improvements

- add topic and schema definition for profiles topic (#307) by @lynnagara
- feat(uptime): Add span_id to check result message (#309) by @evanpurkhiser

## 0.1.93

### Various fixes & improvements

- fix(uptime): Add `subscription_id` and remove monitor related ids (#308) by @wedamija
- feat(uptime): Add timeout example (#305) by @evanpurkhiser

## 0.1.92

### Various fixes & improvements

- fix(uptime): Improve type generation (#306) by @evanpurkhiser

## 0.1.91

### Various fixes & improvements

- ref(uptime): Improve uptime-results schema w/ definitions (#304) by @evanpurkhiser
- feat(issue-search): Add first_release_id to the group_attributes kafka schema (#286) by @snigdhas
- add schema, examples and topic definition for ingest-occurrences (#301) by @lynnagara
- fix(uptime): Bad UUIDs in examples (#302) by @evanpurkhiser
- fix(uptime): Allow request_info and http_status_code to be null (#303) by @evanpurkhiser
- fix snuba-metrics-summaries (#300) by @lynnagara
- ref: remove redundant property from topic files (#299) by @lynnagara
- set 10mb max.message bytes for metrics topics (#298) by @lynnagara

## 0.1.90

### Various fixes & improvements

- add schema, topic definition and examples for ingest-attachments topic (#293) by @lynnagara
- feat(uptime): Add uptime-results topic (#294) by @evanpurkhiser
- ref(format): Match black config with sentry (#297) by @evanpurkhiser
- rename partitions to enforced_partition_count (#296) by @lynnagara
- feat(lint): Add isort (#295) by @evanpurkhiser
- run tests against python 3.12 in CI (#292) by @lynnagara
- bump default python version to 3.11 (#291) by @lynnagara

## 0.1.89

### Various fixes & improvements

- feat: snuba-queries is 50mb (#290) by @lynnagara
- processed-profiles and profiles-call-tree have 50mb (#289) by @lynnagara
- fix ingest-replay-recordings topic definition (#288) by @lynnagara
- fix message.timestamp.type on 3 topics (#287) by @lynnagara

## 0.1.88

### Various fixes & improvements

- set correct segment.bytes on outcomes topics (#285) by @lynnagara
- fix snuba-spans max.message.bytes (#284) by @lynnagara
- fix max.message.bytes on ingest-replay-events (#283) by @lynnagara
- build(deps): bump black from 22.6.0 to 24.3.0 in /python (#240) by @dependabot
- fix: ingest-monitors topic configuration (#282) by @lynnagara

## 0.1.87

### Various fixes & improvements

- introduce standard segment settings for all commit log topics (#281) by @lynnagara
- fix(spans): Fix precise timestamp names in example (#280) by @phacops
- monitors-clock-tick must always have 1 partition (#279) by @lynnagara

## 0.1.86

### Various fixes & improvements

- fix(spans): Fix timestamp names to reflect better their use (#278) by @phacops

## 0.1.85

### Various fixes & improvements

- feat(spans): Add microsecond precision timestamps (#276) by @phacops
- fix: Move default rule to the top of the file (#277) by @phacops

## 0.1.84

### Various fixes & improvements

- set max message bytes on snuba-metrics and snuba-dead-letter-metrics to 10mb (#275) by @lynnagara
- fix: max.message.bytes for dlq topics (#273) by @lynnagara

## 0.1.83

### Various fixes & improvements

- fix(profiles): Add missing configuration option for snuba-profile-chunks (#274) by @phacops

## 0.1.82

### Various fixes & improvements

- feat(profiles): Add schema definition for profile chunks (#272) by @phacops

## 0.1.81

### Various fixes & improvements

- feat(generic-metrics): Add support for zstd compression in message processing (#270) by @ayirr7

## 0.1.80

### Various fixes & improvements

- feat(metrics): Add received_at timestamp to Kafka schema (#271) by @iambriccardo

## 0.1.79

### Various fixes & improvements

- feat: Add missing event-replacements topic (#268) by @lynnagara
- Make retention.ms a mandatory field (#269) by @lynnagara
- feat: Update max message size on buffered-spans (#248) by @shruthilayaj

## 0.1.78

### Various fixes & improvements

- feat(crons): Ensure monitor_environment_id in all clock tasks (#264) by @evanpurkhiser

## 0.1.76

### Various fixes & improvements

- feat(generic-metrics): Switch Kafka schema examples to non-padded Base64 encoding (#267) by @ayirr7
- Add priority to group attributes schema (#251) by @snigdhas

## 0.1.75

### Various fixes & improvements

- perf: change payload type of replay event (#265) by @anonrig
- style(crons): Spelling of timed out (#263) by @evanpurkhiser
- fix: Don't block ci on sphinx warning (#262) by @lynnagara
- fix: ingest-feedback-events-dlq max.message.bytes (#260) by @lynnagara
- fix: Upgrade typify to unblock CI (#261) by @lynnagara

## 0.1.74

### Various fixes & improvements

- feat(crons): Add topic to support monitor clock tasks (#259) by @evanpurkhiser
- feat(crons): Add monitors-clock-tick (#258) by @evanpurkhiser

## 0.1.73

### Various fixes & improvements

- ref(crons): Allow null for sdk property (#257) by @evanpurkhiser

## 0.1.72

### Various fixes & improvements

- Revert "Revert "feat(generic-metrics): Add base64 support to metrics schemas …" (#256) by @ayirr7

## 0.1.71

### Various fixes & improvements

- feat(generic-metrics): Add gauges subscription topic (#249) by @ayirr7

## 0.1.70

### Various fixes & improvements

- feat(crons): Add ingest-monitors schema / topic (#253) by @evanpurkhiser
- style: Spacing (#254) by @evanpurkhiser
- Revert "feat(generic-metrics): Add base64 support to metrics schemas (#252)" (#255) by @ayirr7

## 0.1.69

### Various fixes & improvements

- feat(generic-metrics): Add base64 support to metrics schemas (#252) by @ayirr7

## 0.1.68

### Various fixes & improvements

- ref: clean up sessions-subscription-results topic (#246) by @lynnagara
- feat: Add required partition count to topic definition (#250) by @lynnagara
- feat: Add a DLQ for buffered segment topic (#247) by @shruthilayaj
- test(replay): add example for replay viewed events (#245) by @aliu3ntry

## 0.1.67

### Various fixes & improvements

- feat: Add the scheduled subscription topics (#243) by @lynnagara
- feat: add missing dlq for generic-events (#244) by @lynnagara

## 0.1.66

### Various fixes & improvements

- fix: Don't fail on msgpack topics (#242) by @lynnagara

## 0.1.65

### Various fixes & improvements

- fix: Fix topic creation config (#241) by @lynnagara

## 0.1.64

### Various fixes & improvements

- Add DLQ topics (#239) by @lynnagara

## 0.1.63

### Various fixes & improvements

- feat(spans): Add topic definition for buffered-segment topic (#237) by @shruthilayaj

## 0.1.62

### Various fixes & improvements

- feat(feedback): add feedback-events DLQ (#238) by @aliu3ntry

## 0.1.61

### Various fixes & improvements

- Include empty and null `trace_id` (#235) by @xurui-c
- ref: Add compression.type to ingest-feedback-events (#236) by @lynnagara
- feat: Ensure compression.type is specified on all topics (#234) by @lynnagara
- feat(replay): Config new ingest-feedback-events topic (#227) by @aliu3ntry

## 0.1.60

### Various fixes & improvements

- feat: Add basic schema and examples for ingest-events [INC-660] (#230) by @lynnagara
- feat: Add max.message.bytes on events and transactions topics (#233) by @lynnagara
- meta: fix ingest code owners (#232) by @Dav1dde

## 0.1.59

### Various fixes & improvements

- feat: Add retention values to DLQ (#228) by @lynnagara
- Switch workflow team for issues team (#229) by @armenzg
- ref: Add team ops as codeowners (#226) by @lynnagara
- feat: Add dlq topics to topic registry (#225) by @lynnagara
- feat: Add outcomes-billing topic (#224) by @lynnagara

## 0.1.58

### Various fixes & improvements

- Add encoded series to metrics schemas (#222) by @john-z-yang
- Upgrade to FSL-1.1 (#223) by @chadwhitacre
- Revert "Revert "remove value validation for indexer schema (#220)"" (8ad83926) by @untitaker

## 0.1.57

### Various fixes & improvements

- Revert "remove value validation for indexer schema (#220)" (17219c0e) by @john-z-yang

## 0.1.56

### Various fixes & improvements

- fix: Fix errors schema again (#221) by @untitaker

## 0.1.55

### Various fixes & improvements

- remove value validation for indexer schema (#220) by @john-z-yang

## 0.1.54

### Various fixes & improvements

- ref: Import errors schema from Snuba (#219) by @untitaker
- feat: Export list_topics (#218) by @lynnagara

## 0.1.52

### Various fixes & improvements

- feat: Expose list_topics function (#217) by @lynnagara

## 0.1.51

### Various fixes & improvements

- feat: Topic config (#214) by @lynnagara
- fix: Better output messages when adding properties (#216) by @untitaker
- feat(replays): Add replay-video attribute to recording message (#215) by @cmanallen

## 0.1.50

### Various fixes & improvements

- feat(replays): add replay event to recording schema (#213) by @JoshFerge

## 0.1.49

### Various fixes & improvements

- feat(metrics_summaries): Define a schema for metrics summaries (#212) by @phacops
- add sbc spans (#211) by @victoria-yining-huang

## 0.1.48

### Various fixes & improvements

- ref(rust): Add example name to examples (#209) by @untitaker
- add sbc to topics sbc is using (#210) by @victoria-yining-huang

## 0.1.47

### Various fixes & improvements

- fix(rust): Fix spurious topic-not-found due to wrong sorting key (#208) by @untitaker

## 0.1.46

### Various fixes & improvements

- ref(spans): Remove old topic schema (#207) by @phacops
- ref(profiles): Make schema stricter to reflect Rust consumer struct (#206) by @phacops

## 0.1.45

### Various fixes & improvements

- ref: Fix querylog schema (#204) by @untitaker

## 0.1.44

### Various fixes & improvements

- feat(spans): Set received field as mandatory (#203) by @phacops

## 0.1.43

### Various fixes & improvements

- fix(functions): Remove unneeded fields from the functions schema (#202) by @phacops

## 0.1.42

### Various fixes & improvements

- fix(replays): Add event_hash field to archive example event (#201) by @cmanallen

## 0.1.41

### Various fixes & improvements

- ref: Add more codeowners (#200) by @untitaker
- feat(spans): Remove group_raw from the schema as it's not used anymore (#199) by @phacops

## 0.1.40

### Various fixes & improvements

- Embed and expose examples in Rust (#198) by @Swatinem

## 0.1.39

### Various fixes & improvements

- feat(replays): Add react_component_name to click event example (#197) by @cmanallen
- feat(replays): Add examples (#196) by @cmanallen

## 0.1.38

### Various fixes & improvements

- feat(spans): Add a metrics summary field to spans (#195) by @phacops

## 0.1.37

### Various fixes & improvements

- fix(spans): Fix measurements schema on spans (#194) by @phacops

## 0.1.36

### Various fixes & improvements

- feat(spans): Add measurements field (#190) by @phacops

## 0.1.35

### Various fixes & improvements

- Relicense under FSL-1.0-Apache-2.0 (#193) by @chadwhitacre
- Avoid reruns of the build script (#192) by @Swatinem
- Embed Topics/Schemas into Rust crate (#191) by @Swatinem

## 0.1.34

### Various fixes & improvements

- feat(spans): Add a received field to track e2e latency (#189) by @phacops

## 0.1.33

### Various fixes & improvements

- Add gauges to ingest + snuba generic metrics schema (#186) by @ayirr7
- feat(feedback): add feedback as new event type (#187) by @JoshFerge

## 0.1.32

### Various fixes & improvements

- fix(spans): Fix types for integer and number fields (#185) by @phacops
- Update comment (#183) by @dbanda
- feat(rust): Add validate_json() method in Rust (#184) by @lynnagara

## 0.1.31

### Various fixes & improvements

- fix(spans): Fix snuba-spans example (#182) by @phacops

## 0.1.30

### Various fixes & improvements

- feat(spans): Add schema for ingest-spans (#180) by @phacops
- fix(spans): Remove wrong array type (#181) by @phacops
- spans: add profile id (#179) by @dbanda
- feat(CoGS): Add `shared-resources-usage` topic schema (#178) by @rahul-kumar-saini

## 0.1.29

### Various fixes & improvements

- allow new `nel` event type in events topics (#177) by @oioki

## 0.1.28

### Various fixes & improvements

- Revert "Add spans data schema (#153)" (#176) by @lynnagara

## 0.1.27

### Various fixes & improvements

- fix(spans): Fix schema as tags can only be stored as strings (#175) by @phacops

## 0.1.26

### Various fixes & improvements

- fix(spans): Add missing description field (#174) by @phacops

## 0.1.25

### Various fixes & improvements

- parent 4bcfde3655868210dc9c56df2485ffb29cbb8158 (#173) by @dbanda

## 0.1.24

### Various fixes & improvements

- spans only schemas (#172) by @dbanda
- fix: Fix events schema (#170) by @lynnagara

## 0.1.23

### Various fixes & improvements

- fix: Simplify events schemas (#171) by @lynnagara
- feat(querylog): Add schema definition for stats object (#169) by @lynnagara

## 0.1.22

### Various fixes & improvements

- feat(generic-metrics): Add `aggregation_option` field to metrics (#167) by @john-z-yang
- feat: Export timer data type from querylog (#166) by @lynnagara

## 0.1.21

### Various fixes & improvements

- feat: Mark required fields in querylog (#165) by @lynnagara

## 0.1.20

### Various fixes & improvements

- fix(transactions): Make received field required for transactions (#163) by @ayirr7

## 0.1.19

### Various fixes & improvements

- feat(group-attributes): add new topic and schema for group attributes (#164) by @barkbarkimashark

## 0.1.18

### Various fixes & improvements

- fix(ingest-replay-events): Type is not required (#162) by @lynnagara

## 0.1.17

### Various fixes & improvements

- fix(profile-functions): device class should be an int (#161) by @lynnagara

## 0.1.16

### Various fixes & improvements

- feat: Add schemas for profiling Snuba payloads (#160) by @phacops
- fix: Fix replay example (#159) by @lynnagara

## 0.1.15

### Various fixes & improvements

- feat: ingest-replay-events schema (#155) by @lynnagara
- fix(generic-events): There is also a generic type (#158) by @lynnagara

## 0.1.14

### Various fixes & improvements

- feat(generic-events): Fix schema and example (#157) by @lynnagara

## 0.1.13

### Various fixes & improvements

- feat: Add generic-events topic (#154) by @lynnagara
- docs: Re (#156) by @lynnagara
- Add spans data schema (#153) by @dbanda
- docs: Update readme about choosing a version to release (#151) by @lynnagara

## 0.1.12

### Various fixes & improvements

- fix: Fix events schema (#152) by @lynnagara

## 0.1.11

### Various fixes & improvements

- feat(errors): add errors and trace.sampled to schema (#150) by @barkbarkimashark
- feat(replays): Add version field (#149) by @cmanallen

## 0.1.10

### Various fixes & improvements

- feat: Loosen requests in events schema (#147) by @lynnagara
- doc: Generate servicemap from topic definitions (#145) by @untitaker
- ref: Split up ingest-metrics topics (#146) by @untitaker

## 0.1.9

### Various fixes & improvements

- fix(transactions): Standardise tags in transactions to match events (#144) by @lynnagara

## 0.1.8

### Various fixes & improvements

- ref: Bump json-schema-diff (#142) by @untitaker
- fix(transactions): Remove properties incorrectly set to required in trace context (#139) by @lynnagara
- fix(ingest-replay-recordings): Fix consumer service (#141) by @lynnagara
- fix(transactions): measurement.unit is not required (#140) by @lynnagara
- fix(transactions): Fix parent-span-id (#138) by @lynnagara
- fix: Update jsonschema-gentypes (#136) by @untitaker
- ref: reference SENTRY_INTERNAL_APP_ID from vars (#137) by @asottile-sentry

## 0.1.7

### Various fixes & improvements

- fix: Some fixes to make ingest-replay-recordings usable (#135) by @untitaker
- fix: Fix typo in json_schema_changes (#134) by @untitaker
- fix: Adjust breaking changes warning (#133) by @untitaker
- fix: Random snuba crashes found by hypothesis-jsonschema (#132) by @untitaker

## 0.1.6

### Various fixes & improvements

- fix: Exception values is not required (#131) by @lynnagara

## 0.1.5

### Various fixes & improvements

- feat: Add functionality to schema diff script to dump out versions (#130) by @untitaker
- fix: Improve formatting of schema diff further (#129) by @untitaker
- fix: Align sdk property in events and transactions (#125) by @lynnagara
- ref: Bump json-schema-diff to 0.1.5 (#128) by @untitaker
- fix: Deduplicate list of consumers and producers (#127) by @lynnagara
- test: Assert that codec decodes from bytes and encodes into bytes (#126) by @untitaker

## 0.1.4

### Various fixes & improvements

- fix: Make Codec.validate public (#124) by @untitaker

## 0.1.3

### Various fixes & improvements

- feat: JsonCodec and MsgpackCodec are usable without schemas (#123) by @lynnagara
- fix(doc): Document how to use a schema (#121) by @untitaker
- ref(ci): Give more direct advice in schema-changes lint (#118) by @untitaker

## 0.1.2

### Various fixes & improvements

- fix(build): Add missing module to setup.py (#122) by @untitaker

## 0.1.1

### Various fixes & improvements

- ref: Align some fields in events and transactions schemas (#120) by @lynnagara
- fix(events): Fix schema for tombstone event (#119) by @lynnagara

## 0.1.0

### Various fixes & improvements

- feat: Add support for msgpack, add schema for replay-recordings, move arroyo codecs into repo (#116) by @untitaker
- ref: Make everything take additionalProperties (#117) by @untitaker
- release: 0.0.33 (f73a808e) by @getsentry-bot

## 0.0.33

### Various fixes & improvements

- add subdivision (#115) by @udameli

## 0.0.32

### Various fixes & improvements

- fix(events): Loosen events mechanism (#114) by @lynnagara
- ref: Add basic consumer/producer info for each topic (#113) by @untitaker
- fix: Loosen metrics schemas (#112) by @lynnagara

## 0.0.31

### Various fixes & improvements

- feat(metrics): Add sentry_received_timestamp to schemas to support indexer SLO (#109) by @ayirr7
- fix(transactions): Span description can be null (#108) by @lynnagara

## 0.0.29

### Various fixes & improvements

- fix: Fix Rust test breakage and add Rust CI (#107) by @untitaker

## 0.0.28

### Various fixes & improvements

- fix: Fix wording in json-schema-diff (#103) by @untitaker
- fix(transactions): Fix transactions "data" to exclude stuff Snuba doesn't care about (#102) by @lynnagara
- fix: Bump json-schema-diff to 0.1.4 (#101) by @untitaker

## 0.0.27

### Various fixes & improvements

- fix(transactions): Remove some stuff Snuba doesn't care about (#99) by @lynnagara
- fix(events): Fix the schema for tombstone events (#98) by @lynnagara
- fix(rust): Make regress dependency optional as well (#100) by @untitaker

## 0.0.26

### Various fixes & improvements

- fix: Make generated schema types an optional feature (#96) by @untitaker
- fix: Impl std::error::Error for SchemaError (#95) by @untitaker
- fix: Bump json-schema-diff to 0.1.2 (#94) by @untitaker
- docs: Clarify that bumping the version is part of the release process (#92) by @lynnagara
- feat: Remove unused fields from subscription results (#88) by @lynnagara
- ref: Loosen transaction schema (#93) by @lynnagara

## 0.0.25

### Various fixes & improvements

- feat: Add Rust build cache to reduce CI times (#89) by @untitaker
- fix: Align snuba-metric value field with ingest-metrics (#90) by @untitaker

## 0.0.24

### Various fixes & improvements

- docs: Add some guidance about schema strictness (#91) by @lynnagara
- fix: Loosen transactions schema, add example (#87) by @lynnagara
- fix: Standardise retention_days on events and transactions (#86) by @lynnagara
- fix: Lint against dead schema files unreferenced by any topic (#85) by @untitaker
- fix(events): We seem to be getting transaction_id in end_unmerge now (#79) by @lynnagara
- fix: Make schema-changes workflow faster (#84) by @untitaker

## 0.0.23

### Various fixes & improvements

- fix: Transactions context (#80) by @lynnagara

## 0.0.22

### Various fixes & improvements

- fix: Fix metric value types across all schemas (#83) by @untitaker

## 0.0.21

### Various fixes & improvements

- feat: Transactions topic and schema definition (#77) by @lynnagara
- fix: Improve rust types for ingest-metrics again (#78) by @untitaker
- fix: Fix filename handling of jsonschema changes (#70) by @untitaker

## 0.0.20

### Various fixes & improvements

- feat: Rust types (#74) by @untitaker
- fix: Bump json-schema-diff (#76) by @untitaker
- ref: Update action-migrations workflow, get rid of bogus "SQL" message (#75) by @untitaker

## 0.0.19

### Various fixes & improvements

- ref(metric alerts): Add generic metrics sub results (#73) by @ceorourke

## 0.0.18

### Various fixes & improvements

- fix(outcomes): Update outcome schema (#69) by @john-z-yang
- fix: Remove incorrect property from subscription result schema (#72) by @lynnagara
- docs: Clarify that example messages must be stripped of sensitive data (#71) by @lynnagara

## 0.0.17

### Various fixes & improvements

- feat: Release rust library (#68) by @untitaker
- feat: Add CI to detect breaking changes (#67) by @untitaker

## 0.0.16

### Various fixes & improvements

- fix: Subscription result schema (#65) by @lynnagara

## 0.0.15

### Various fixes & improvements

- update outcomes schema (#66) by @john-z-yang
- fix(events): Boolean request data (#64) by @lynnagara

## 0.0.14

### Various fixes & improvements

- ref(subscription results): Make version a const (#63) by @ceorourke
- feat(examples): Ensure all examples are json (#58) by @lynnagara

## 0.0.13

### Various fixes & improvements

- fix(outcomes): Add code owner for outcomes (#62) by @john-z-yang
- fix: Remove Cargo.lock (#61) by @untitaker
- ref(outcomes): Add outcomes schema (#55) by @john-z-yang

## 0.0.12

### Various fixes & improvements

- feat: Define codeowner for ingest-metrics (#60) by @lynnagara
- feat: Schema ownership (#59) by @lynnagara
- feat: Add ingest-metrics topic (#56) by @untitaker
- feat: Implement versions for get_schema in Rust (#57) by @untitaker

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
