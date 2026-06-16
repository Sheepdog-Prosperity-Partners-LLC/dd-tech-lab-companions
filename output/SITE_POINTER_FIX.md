# DD Tech Lab Site Pointer Fix

Prepared by Noah Green CPA CFE.

Date checked: 2026-06-16.

## Finding

The live DD Tech Lab index pages still point to the archived personal companion repository:

```text
https://github.com/noahrgreen/dd-tech-lab-companion
```

Observed on:

- https://sheepdogprosperitypartners.com/dd-tech-lab/
- https://sheepdogprosperitypartners.com/dd-tech-lab/page/2/
- https://sheepdogprosperitypartners.com/dd-tech-lab/page/3/
- https://sheepdogprosperitypartners.com/dd-tech-lab/page/4/

## Required WordPress Edit

Edit the DD Tech Lab page module labeled "Code Repository" and replace the archived pointer with:

```text
https://github.com/Sheepdog-Prosperity-Partners-LLC/dd-tech-lab-companions
```

Do not point readers to the singular `dd-tech-lab-companion` repository or to the archived national-security standalone repository.

## Post-Edit Check

After the WordPress edit, refresh all DD Tech Lab index pages and confirm the old URL no longer appears in the page source.
