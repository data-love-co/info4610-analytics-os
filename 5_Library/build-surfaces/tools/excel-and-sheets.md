---
title: "Excel / Google Sheets"
level: "Beginner"
best_for: "Recipients who live in spreadsheets and need to change it themselves"
---

# Excel / Google Sheets

Not a lesser option. For a large share of the people in this room it is the correct one.

**What it's for here:** when your recipients live in spreadsheets, when they need to change the model
themselves, and when the thing has to keep working while you're on vacation.

**Cost:** you already have it.

**Quickstart with an agent**

1. Have Claude produce the calculation logic and a clean output table
2. Ask for it as a spreadsheet with an input block at the top and formulas below
3. Check three numbers by hand against the analysis document
4. Write the definitions into the sheet itself, not into a separate document nobody opens

**The rules if you build here**

- **Formulas visible.** No hidden sheets, no hardcoded numbers buried inside a formula. The reason
  spreadsheets endure is transparency — a spreadsheet with a magic constant in cell M47 is worse than
  a script
- **Inputs in one block**, clearly labeled and visually distinct. Everything else calculated
- **Definitions in the sheet.** A metric without its definition gets misread by the second person who
  opens it
- **Source and date in a corner.** In eight months someone will find this and need to know what it
  was built from

**Watch out for:** Excel silently reformats things. Leading zeros vanish from IDs and ZIP codes, long
numbers become scientific notation, and anything resembling a date becomes one — including gene
names and version numbers. Check your key columns after any round trip through a spreadsheet.
