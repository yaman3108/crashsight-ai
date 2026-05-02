# Security Policy

## Reporting Sensitive Detections

CrashSight AI analyses satellite imagery to detect potential crash sites. Some detections may involve sensitive situations that require careful handling.

### If You Find a Potentially Recent Crash Site

If a detection appears to represent a **recent, active emergency** (evidence of a crash that may have occurred within the past 72 hours):

1. **Do not publish it.** Do not post it in Issues, Discussions, or anywhere public.
2. **Contact a project maintainer immediately** via email (see below).
3. The maintainer will evaluate whether relevant authorities (aviation authority, coast guard, etc.) should be notified.
4. The detection will be documented internally with a record of any actions taken.

### If You Find a Detection Near Protected or Sacred Land

If a detection falls within indigenous land, protected areas, or culturally sensitive sites:

1. Flag it as `NEEDS_REVIEW` in the dataset.
2. Do not publish coordinates or imagery until reviewed by a maintainer.
3. Consult relevant local guidelines before any further action.

## Reporting Security Vulnerabilities

If you discover a security vulnerability in the codebase (e.g., API key exposure, data leak, injection vulnerability):

1. **Do not open a public issue.**
2. Email the maintainers at: `[MAINTAINER_EMAIL]` (replace with your actual email when publishing).
3. Include a description of the vulnerability and steps to reproduce it.
4. We will acknowledge receipt within 48 hours and work on a fix.

## What Is NOT a Security Issue

- False positive detections (use the regular issue tracker).
- Feature requests or bug reports (use GitHub Issues).
- Questions about the project (use GitHub Discussions).

## Responsible Disclosure

We follow responsible disclosure practices. If you report a vulnerability, we ask that you give us reasonable time to address it before making it public.
