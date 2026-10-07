/**
 * MAI KỲ HÀ SEAFOOD — website inquiry receiver.
 *
 * Lives inside the Google Sheet "Yêu cầu từ website maikyha.com" (Extensions → Apps Script).
 * Deployed as a web app (Execute as: me, Who has access: Anyone).
 * Each inquiry sent from the website's contact form becomes one row in the sheet,
 * and a notification email goes to the account that owns the sheet.
 */
var HEADERS = ['Thời gian', 'Ngôn ngữ', 'Nhu cầu', 'Sản phẩm', 'Người liên hệ', 'Doanh nghiệp',
               'Email / Điện thoại', 'Khối lượng', 'Điểm giao', 'Nội dung', 'Trang gửi'];

function doPost(e) {
  var p = (e && e.parameter) || {};
  // Hidden field that people never see; automated spam fills it in.
  if (p.website) return reply_('ok');
  if (!p.name || !p.contact || !p.message) return reply_('missing');

  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.setFrozenRows(1);
      sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    }
    var row = [new Date(), p.lang === 'en' ? 'English' : 'Tiếng Việt', clip_(p.need), clip_(p.product),
               clip_(p.name), clip_(p.company), clip_(p.contact), clip_(p.quantity), clip_(p.destination),
               clip_(p.message, 2500), clip_(p.page)];
    sheet.appendRow(row.map(safe_));
  } finally {
    lock.releaseLock();
  }

  var owner = Session.getEffectiveUser().getEmail();
  var lines = HEADERS.slice(1).map(function (h, i) { return h + ': ' + (clip_([p.lang, p.need, p.product, p.name, p.company, p.contact, p.quantity, p.destination, p.message, p.page][i], 2500) || '—'); });
  var mail = {
    to: owner,
    subject: 'Yêu cầu mới từ website: ' + clip_(p.company || p.name, 80),
    body: 'Có yêu cầu mới gửi từ maikyha.com\n\n' + lines.join('\n') + '\n\nXem toàn bộ: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl()
  };
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(p.contact || '')) mail.replyTo = p.contact.trim();
  MailApp.sendEmail(mail);
  return reply_('ok');
}

function doGet() { return reply_('ready'); }

function clip_(v, n) { return String(v == null ? '' : v).trim().slice(0, n || 300); }
// Stop a value starting with = + - @ from being read as a spreadsheet formula.
function safe_(v) { return typeof v === 'string' && /^[=+\-@]/.test(v) ? "'" + v : v; }
function reply_(status) {
  return ContentService.createTextOutput(JSON.stringify({ status: status })).setMimeType(ContentService.MimeType.JSON);
}
