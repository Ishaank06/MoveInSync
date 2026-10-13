# MoveInSync FDE Case Study Solution

This repository contains my submission for the MoveInSync Forward Deployed Engineer case study on improving Play Store ratings.

## Files

- `MoveInSync_FDE_Case_Study_Submission.pdf` - main case study submission.
- `MoveInSync_FDE_Case_Study_Submission.md` - editable text version with full source links.
- `MoveInSync_FDE_Case_Study_Presentation.pptx` - short interviewer-friendly presentation.
- `play_pulse.py` - runnable public Play Store review pulse script.
- `pulse_snapshots/2026-10-13.json` - snapshot from the script run.
- `Submission_Form_Answers.md` - exact links and short note used for the application form.

## Core Recommendation

MoveInSync should treat Play Store rating improvement as a commute-trust recovery problem. The highest-impact work is to reduce moments where an employee feels stranded or wrongly blamed: booking confirmation, live tracking freshness, check-in/no-show recovery, OTP visibility, app reliability, and support closure.

## What I Built

The solution includes:

- Public review signal diagnosis.
- Rating math to show why review prompts alone will not move the rating enough.
- A runnable Play Store pulse script with a dated snapshot.
- Prioritized product and engineering fixes.
- A no-show configuration audit based on MoveInSync's public Driver App 6.4.0 help-center article.
- Release guardrails for staged rollout and halt rules.
- A reusable "Ratings Room" system for recurring review monitoring.
- A 30/60/90-day execution plan.
- Metrics, public reply examples, assumptions, and tools used.

## Script Output

I ran:

```bash
python play_pulse.py --app com.moveinsync.ets --snapdir pulse_snapshots
```

The 2026-10-13 snapshot read 235 written reviews from the last 30 days and 223 from the prior 30 days. It reported a Play score of 4.6386456 from 114,886 ratings, a last-30-day written-review average of 3.75, and a 27.7% 1-star share. Top 1-star versions were 12.19.0, 12.18.1 and unknown.

## Tools And Sources Used

I used public data only, as requested in the assignment:

- MoveInSync assignment PDF and FDE JD PDF.
- Google Play public listing.
- AppBrain public app profile.
- Chrome-Stats public review sample.
- Apple App Store listing.
- MoveInSync public Driver App 6.4.0 help-center article.
- Public competitor listings for Routematic and eFmFm.
- Google Play documentation for reviews, replies, Play Console analysis, and the In-App Review API.
- AI assistance to structure the research, classify public review themes, and turn the recommendation into a polished field memo and deck.

## Notes

The recommendation should be validated in week 1 with internal data: Play Console exports, Android vitals, crash logs, support tickets, trip logs, routing telemetry, and customer transport desk feedback.
