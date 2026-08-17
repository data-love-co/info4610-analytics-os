# Chart Choices

A chart is an argument. Choosing the wrong form doesn't just look bad — it makes a different
argument than the one your data supports.

---

## Pick by the question, not by the data type

| The question | Chart |
|---|---|
| How has this changed over time? | Line |
| How do these categories compare? | Horizontal bar, sorted by value |
| What's the composition of a whole? | Stacked bar, or just a table |
| How are these two things related? | Scatter |
| How is this distributed? | Histogram, or box plot for comparing groups |
| Where does this stand vs. target? | Bullet chart, or a bar with a target line |
| How big is the difference, and how sure are we? | Point with error bars |

**When in doubt, use a table.** Five numbers in a clean table beat five numbers in a chart. Charts
earn their place when there are enough values that pattern-recognition beats reading — usually a
dozen or more.

---

## The rules that matter most

**Start bars at zero. Always.** A bar chart encodes value as length. Truncating the axis makes a 2%
difference look like a cliff. This is the single most common misleading chart in business, and it's
usually not deliberate — someone let the tool auto-scale.

**Line charts may start above zero** when the variation is what matters, but mark it and say so.

**Sort bars by value**, not alphabetically, unless the categories have an inherent order (months,
sizes, tiers). Sorting is free and it does the reader's work for them.

**One y-axis.** Dual axes let you manufacture a relationship between any two series by choosing the
scales. If two things need different scales, stack two charts with a shared x-axis.

**Label directly** where you can. A line labeled at its end beats a legend the reader has to
cross-reference.

**Put units and the time window on the chart**, not just in the surrounding text. Charts get
screenshotted and pasted into decks without their context, every time.

---

## What to avoid, and why

| Avoid | Because |
|---|---|
| Pie charts with more than 4 slices | People can't compare angles. Use a sorted bar chart |
| Any 3D chart | Perspective distorts the encoding. There is no exception |
| Dual y-axes | Implies a relationship you constructed by choosing scales |
| Truncated bar axes | Exaggerates differences — the most common misleading chart in business |
| Rainbow color scales | Not perceptually uniform; creates boundaries that aren't in the data |
| Red/green as the only distinction | Roughly 1 in 12 men can't reliably distinguish them |
| A chart for 3 numbers | A sentence is faster |
| Connecting unordered categories with a line | Lines imply continuity. Categories aren't continuous |

---

## Color

**Use the fewest colors that do the job.** Grey for context, one accent color for the thing you want
looked at. A chart where everything is colored is a chart with no emphasis.

**Encode by meaning:**

- **Categorical** — distinct hues, at most six. Beyond that, group the tail into "other"
- **Sequential** — one hue, varying lightness. Low to high
- **Diverging** — two hues meeting at a meaningful midpoint (zero, target, average)

**Never rely on color alone.** Add a label, a shape, or a pattern so the chart survives colorblind
readers, greyscale printing, and a projector with the contrast turned down.

**Check it in both light and dark.** Half your readers are on a dark theme and a chart designed on
white can be unreadable there.

---

## Showing uncertainty

This is where most business charts fail — the analysis had a range and the chart shows a line.

- **Forecasts:** shade the interval, widening with horizon. A forecast band the same width at month
  one and month twelve wasn't built from data.
- **Comparisons:** point with error bars, plus a reference line at zero. This single chart carries an
  entire A/B readout.
- **Distributions:** show the distribution rather than the mean. A box plot or a strip plot tells the
  reader what an average hides.
- **Small samples:** put the n on the chart. "82% (n=11)" prevents a real misread.

---

## The ninety-second test

An executive dashboard gets about ninety seconds. Check:

1. Is it obvious what this shows, within ten seconds, without narration?
2. Is the most important thing the most visually prominent thing?
3. Can someone tell whether the direction is good or bad without being told?
4. Are the units, the time window, and the source on the chart?
5. Would a screenshot of just this chart, with no context, still be honest?

Question five is the one people skip, and screenshots of charts travel further than the documents
they came from.
