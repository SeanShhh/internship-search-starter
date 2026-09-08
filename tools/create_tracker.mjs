import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const output = process.argv[2] || "tracker/Internship Search Tracker.xlsx";
const workbook = Workbook.create();
const dashboard = workbook.worksheets.add("Dashboard");
const applications = workbook.worksheets.add("Applications");
const outreach = workbook.worksheets.add("Outreach");

const navy = "#17365D";
const paleBlue = "#D9EAF7";
const paleYellow = "#FFF2CC";
const paleRed = "#FCE4D6";
const statuses = ["Discovered", "Preparing", "Ready to apply", "Applied", "Interviewing", "Offers", "Closed", "Flagged", "Skipped"];

function title(sheet, text, endColumn) {
  sheet.showGridLines = false;
  sheet.getRange(`A2:${endColumn}2`).merge();
  sheet.getRange("A2").values = [[text]];
  sheet.getRange("A2").format = { font: { name: "Arial", size: 14, bold: true, color: "#000000" } };
  sheet.getRange(`A3:${endColumn}3`).format.borders = { bottom: { style: "thin", color: navy } };
}
function header(range) {
  range.format = { fill: navy, font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true };
}

title(dashboard, "Internship search dashboard", "H");
dashboard.getRange("A5:B5").values = [["Metric", "Count"]];
header(dashboard.getRange("A5:B5"));
dashboard.getRange("A6:A14").values = statuses.map((status) => [status]);
dashboard.getRange("B6").formulas = [["=COUNTIFS(Applications!$J$6:$J$205,A6)"]];
dashboard.getRange("B6:B14").fillDown();
dashboard.getRange("D5:E5").values = [["Next action", "Due date"]];
header(dashboard.getRange("D5:E5"));
dashboard.getRange("D6:E10").values = [["Use Applications filters to review actions", ""], ["", ""], ["", ""], ["", ""], ["", ""]];
dashboard.getRange("G5:H5").values = [["How to use this workbook", ""]];
header(dashboard.getRange("G5:H5"));
dashboard.getRange("G6:H10").merge();
dashboard.getRange("G6").values = [["Applications and Outreach are the source records. This dashboard is derived from them. Edit status, dates, and next actions in the source sheets. Keep an application ID unchanged as its folder moves."]];
dashboard.getRange("G6").format.wrapText = true;
dashboard.getRange("A5:B14").format.borders = { preset: "all", style: "thin", color: "#D9D9D9" };
dashboard.getRange("D5:E10").format.borders = { preset: "all", style: "thin", color: "#D9D9D9" };
dashboard.getRange("G5:H10").format.borders = { preset: "all", style: "thin", color: "#D9D9D9" };
dashboard.getRange("A6:A14").format.fill = paleBlue;
dashboard.getRange("A:A").format.columnWidth = 20;
dashboard.getRange("B:B").format.columnWidth = 12;
dashboard.getRange("D:D").format.columnWidth = 34;
dashboard.getRange("E:E").format.columnWidth = 14;
dashboard.getRange("G:G").format.columnWidth = 23;
dashboard.getRange("H:H").format.columnWidth = 23;
dashboard.getRange("G6:H10").format.rowHeight = 23;

title(applications, "Applications", "T");
applications.getRange("A4:T4").values = [["Workbook status is authoritative. Use one permanent ID per role; keep folder link and next action current. Record posting verification and unknown eligibility rather than guessing.", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]];
applications.getRange("A4:T4").merge();
applications.getRange("A4").format = { font: { italic: true, color: "#666666", size: 10 }, wrapText: true };
const appHeaders = ["Application ID", "Employer", "Role", "Location", "Program / term", "Source URL", "Posting verified", "Eligibility", "Deadline", "Status", "Priority", "Folder link", "Materials ready", "Submission evidence", "Applied date", "Last updated", "Next action", "Next action due", "Duplicate check", "Notes"];
applications.getRange("A5:T5").values = [appHeaders];
header(applications.getRange("A5:T5"));
applications.getRange("A6:T6").values = [["APP-0001", "Northstar Labs", "Product Operations Intern", "Remote", "Summer 2027", "https://careers.example.org/northstar/product-operations-intern", new Date("2026-09-07"), "Needs confirmation", new Date("2026-10-15"), "Discovered", "Medium", "../applications/discovered/APP-0001-northstar-product-operations-intern/", "No", "", "", new Date("2026-09-07"), "Review eligibility and role fit", new Date("2026-09-12"), "No duplicate found", "Fictional example"]];
applications.getRange("A6:T205").format.font = { name: "Arial", size: 10, color: "#000000" };
applications.getRange("A5:T205").format.verticalAlignment = "center";
applications.getRange("F6:F205").format.wrapText = true;
applications.getRange("T6:T205").format.wrapText = true;
applications.getRange("G6:G205").format.numberFormat = "mm/dd/yy";
applications.getRange("I6:I205").format.numberFormat = "mm/dd/yy";
applications.getRange("O6:O205").format.numberFormat = "mm/dd/yy";
applications.getRange("P6:P205").format.numberFormat = "mm/dd/yy";
applications.getRange("R6:R205").format.numberFormat = "mm/dd/yy";
applications.getRange("J6:J205").dataValidation = { rule: { type: "list", values: statuses } };
applications.getRange("M6:M205").dataValidation = { rule: { type: "list", values: ["No", "Draft", "Ready", "Submitted"] } };
applications.getRange("H6:H205").dataValidation = { rule: { type: "list", values: ["Confirmed eligible", "Needs confirmation", "Not eligible"] } };
applications.getRange("K6:K205").dataValidation = { rule: { type: "list", values: ["High", "Medium", "Low"] } };
applications.getRange("J6:J205").conditionalFormats.add("containsText", { text: "Flagged", format: { fill: paleRed, font: { bold: true, color: "#9C0006" } } });
applications.getRange("R6:R205").conditionalFormats.add("cellIs", { operator: "lessThan", formula: "=TODAY()", format: { fill: paleYellow, font: { bold: true } } });
applications.freezePanes.freezeRows(5);
for (const [col, width] of [["A:A", 15], ["B:B", 20], ["C:C", 28], ["D:D", 16], ["E:E", 16], ["F:F", 36], ["G:G", 14], ["H:H", 20], ["I:I", 13], ["J:J", 16], ["K:K", 12], ["L:L", 32], ["M:M", 15], ["N:N", 20], ["O:O", 13], ["P:P", 13], ["Q:Q", 34], ["R:R", 14], ["S:S", 18], ["T:T", 28]]) applications.getRange(col).format.columnWidth = width;

title(outreach, "Outreach", "N");
outreach.getRange("A4:N4").values = [["Keep contact evidence in the local SQLite database if you use it. This sheet is authoritative for outreach status and follow-up timing.", "", "", "", "", "", "", "", "", "", "", "", "", ""]];
outreach.getRange("A4:N4").merge();
outreach.getRange("A4").format = { font: { italic: true, color: "#666666", size: 10 }, wrapText: true };
const outreachHeaders = ["Outreach ID", "Application ID", "Contact name", "Organization", "Relationship", "Contact evidence", "Channel", "Draft status", "Sent date", "Reply date", "Follow-up due", "Status", "Next action", "Notes"];
outreach.getRange("A5:N5").values = [outreachHeaders];
header(outreach.getRange("A5:N5"));
outreach.getRange("A6:N6").values = [["OUT-0001", "APP-0001", "Jordan Example", "Northstar Labs", "Existing relationship", "Met through campus product club", "Email", "Draft", "", "", new Date("2026-09-14"), "Draft", "Review message before sending", "Fictional example"]];
outreach.getRange("H6:H205").dataValidation = { rule: { type: "list", values: ["No draft", "Draft", "Ready for review", "Sent"] } };
outreach.getRange("L6:L205").dataValidation = { rule: { type: "list", values: ["Draft", "Sent", "Replied", "Closed"] } };
outreach.getRange("I6:K205").format.numberFormat = "mm/dd/yy";
outreach.getRange("A5:N205").format.verticalAlignment = "center";
outreach.getRange("F6:F205").format.wrapText = true;
outreach.getRange("N6:N205").format.wrapText = true;
outreach.freezePanes.freezeRows(5);
for (const [col, width] of [["A:A", 14], ["B:B", 15], ["C:C", 20], ["D:D", 20], ["E:E", 20], ["F:F", 30], ["G:G", 12], ["H:H", 17], ["I:K", 13], ["L:L", 14], ["M:M", 30], ["N:N", 26]]) outreach.getRange(col).format.columnWidth = width;

workbook.recalculate();
const outputFile = await SpreadsheetFile.exportXlsx(workbook);
await fs.mkdir(new URL(".", `file://${process.cwd()}/${output}`).pathname, { recursive: true }).catch(() => {});
await outputFile.save(output);
const inspect = await workbook.inspect({ kind: "table", range: "Dashboard!A5:H14", include: "values,formulas", tableMaxRows: 15, tableMaxCols: 8 });
console.log(inspect.ndjson);
