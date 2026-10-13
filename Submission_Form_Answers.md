# Paste-Ready Submission Form Answers

## Submission Link(s)

```text
https://github.com/Ishaank06/MoveInSync, https://github.com/Ishaank06/MoveInSync/blob/main/MoveInSync_FDE_Case_Study_Submission.pdf, https://github.com/Ishaank06/MoveInSync/blob/main/MoveInSync_FDE_Case_Study_Submission.md, https://github.com/Ishaank06/MoveInSync/blob/main/play_pulse.py
```

## Related PPT Link / Demo Video Link / Other Demo Link(s) / Project Link

```text
https://github.com/Ishaank06/MoveInSync/blob/main/MoveInSync_FDE_Case_Study_Presentation.pptx, https://github.com/Ishaank06/MoveInSync/blob/main/pulse_snapshots/2026-10-13.json
```

## Short Note On How I Got There And Tools Used

```text
I treated the assignment as a recurring FDE problem, not a one-time product audit. I started from the employee commute journey in the case prompt, then reviewed public signals from the MoveInSync Google Play listing, AppBrain, Chrome-Stats review samples, Apple App Store, competitor listings, MoveInSync's public Driver App 6.4.0 help-center article, and Google Play documentation. I grouped negative review themes by commute stage and severity, then prioritized fixes that reduce high-stress rating events: booking confidence, live tracking freshness, no-show recovery, OTP visibility, app reliability, and support closure.

I also added and ran a small Python script, `play_pulse.py`, to make the Ratings Room idea concrete. On 2026-10-13 it read 235 written reviews from the last 30 days and 223 from the prior 30 days, reporting a 27.7% 1-star share and version spikes in 12.19.0 and 12.18.1. I used AI tools to speed up research structuring, theme clustering, rating-math reasoning, and document formatting. The final recommendation is packaged as a field memo, a short PPT, editable Markdown, a runnable script, and a dated JSON snapshot.
```

## Any Other Relevant Link

Use this for supporting artifacts.

```text
https://github.com/Ishaank06/MoveInSync/blob/main/README.md, https://github.com/Ishaank06/MoveInSync/blob/main/Submission_Form_Answers.md
```

## Recommended Upload Checklist

1. Open each GitHub link in an incognito browser tab to confirm it works without login.
2. Paste the repo link, PDF link, Markdown link, and script link into the submission field.
3. Paste the PPT link and JSON snapshot link into the related links field.
4. If there is time, record a 2-minute Loom/Drive walkthrough and add that link too.

## 2-Minute Demo Video Script

```text
Hi, I am walking through my MoveInSync FDE case study submission.

My main conclusion is that Play Store ratings should be treated as a commute-trust recovery problem, not only an app UX problem. Public reviews suggest that users get most frustrated when they feel stranded or wrongly blamed during booking, live tracking, check-in, no-show, OTP, or support moments.

I prioritized three first fixes: a persistent trip status card, a no-show recovery flow, and tracking freshness instrumentation. These are specific enough for Product and Engineering to start the next day.

I also added a small working script called play_pulse.py. It pulled 235 written reviews from the last 30 days and flagged a 27.7% 1-star share, with version spikes in 12.19.0 and 12.18.1.

The 30/60/90-day plan starts with review ingestion, a no-show configuration audit, staged rollout guardrails, and pilots. It then scales the validated fixes and launches ethical in-app review prompts after successful commute moments.
```
