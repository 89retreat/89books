# Review — CV1.DS2.US2

## Status

Reviewed

## Debt Findings

- Browser layout JavaScript (rows, collapse, column balancing) has no automated test; checked by hand at four widths
- Face-out cover width duplicated between CSS (154/133 px plus margins) and JavaScript (164/143)
- Full generation with cover-scan rejection and final layout not yet exercised on a real paid run
- First generation downloads every cover once to check it (cached afterwards)

## Debt Decision

defer

## Defer Reason

Template will likely change when the shelf is served by URL; the next real run happens in US3; extra time is acceptable for founder validation

## Revisit Trigger

CV1.DS3 or CV2 serving the shelf by URL (layout tests, shared width); US3 real run (full generation)

## Missing Decision

- none
