from html import escape
import re

# Product descriptions stay within the supplied catalog; commercial specifications
# are confirmed per order rather than inferred from a photograph.
product_focus={
'ca-chem':('Cá chẽm trong danh mục MAI KỲ HÀ','Khi hỏi hàng cá chẽm, hãy nêu kích cỡ mong muốn, dạng nguyên con hoặc yêu cầu xử lý, cùng khối lượng và cách đóng gói. Ảnh bên dưới giúp bạn đối chiếu mặt hàng trước khi trao đổi.'),
'muc-xa-den':('Mực xà đen — hình ảnh và yêu cầu hỏi hàng','Với mực xà đen, cần làm rõ dạng hàng, mức độ xử lý, kích cỡ và quy cách đóng gói. Bạn có thể gửi ảnh tham khảo kèm yêu cầu để hai bên thống nhất đúng sản phẩm.'),
'ca-ngu-o':('Trao đổi nhu cầu cá ngừ ồ','Hãy ghi rõ cá ngừ ồ khi gửi yêu cầu để phân biệt với các dòng cá ngừ khác trong danh mục. Bổ sung kích cỡ, dạng xử lý, mục đích sử dụng và khối lượng dự kiến.'),
'ca-chim-den':('Tìm hiểu mặt hàng cá chim đen','Xem ảnh thực tế và mô tả kích cỡ, dạng hàng bạn cần. Khi có yêu cầu riêng về xử lý, phân loại hoặc đóng kiện, hãy đưa vào nội dung hỏi hàng để được trao đổi cụ thể.'),
'ca-nuc-hgt':('Cá nục gai cắt đầu cho nhu cầu nguyên liệu','Mặt hàng được giới thiệu cho nhu cầu nguyên liệu đóng hộp. Khi hỏi hàng, hãy mô tả yêu cầu xử lý, phân cỡ và quy cách đóng gói; các tiêu chí cụ thể cần được thống nhất theo đơn hàng.'),
'ca-liet-chi-vang':('Đối chiếu đúng mặt hàng cá liệt chỉ vàng','Gửi tên mặt hàng kèm kích cỡ, dạng xử lý và hình ảnh tham khảo nếu có. Thông tin về khối lượng, đóng gói và lịch giao giúp việc trao đổi phương án sát nhu cầu hơn.'),
'ca-banh-lai-trang':('Cá bánh lái trắng trong danh mục','Bạn có thể tham khảo các ảnh thực tế bên dưới để nhận diện mặt hàng. Vui lòng bổ sung kích cỡ mong muốn, dạng xử lý, khối lượng mỗi kiện và địa điểm giao khi hỏi mua.'),
'ca-trao-mat-to':('Trao đổi đúng quy cách cá tráo mắt to','Ghi rõ tên cá tráo mắt to, kích cỡ cùng đơn vị phân cỡ và khối lượng cần mua. Nếu dùng làm nguyên liệu, hãy mô tả thêm yêu cầu xử lý để cùng làm rõ quy cách.'),
'ca-song':('Cá sòng — chuẩn bị yêu cầu mua hàng','Ảnh thực tế giúp bạn có cơ sở ban đầu để trao đổi về mặt hàng cá sòng. Quy cách, cách phân cỡ, đóng gói và điều kiện bảo quản được xác nhận riêng theo nhu cầu.'),
'ca-bac-ma':('Trao đổi nhu cầu cá bạc má','Cung cấp kích cỡ, dạng hàng, khối lượng và quy cách đóng kiện mong muốn. Với nhu cầu định kỳ, bạn có thể nêu tần suất dự kiến để hai bên trao đổi kế hoạch phù hợp.'),
'ca-nuc-suon':('Cá nục suôn / cá nục dài','Danh mục sử dụng cả tên cá nục suôn và cá nục dài cho mặt hàng này. Khi hỏi hàng, hãy kèm tên trong danh mục hoặc ảnh tham khảo để tránh nhầm lẫn với các dòng cá nục khác.'),
'ca-nuc-duoi-do':('Lựa chọn đúng dòng cá nục đuôi đỏ','Đối chiếu hình ảnh và ghi rõ cá nục đuôi đỏ trong nội dung hỏi hàng. Kích cỡ, mức độ xử lý, khối lượng và đóng gói là các thông tin cần làm rõ trước khi trao đổi giá.'),
'ca-nuc-tron':('Cá nục tròn / cá nục gai','Mặt hàng được giới thiệu dưới tên cá nục tròn / cá nục gai. Nếu cần dạng cắt đầu cho nhu cầu nguyên liệu, hãy nêu rõ yêu cầu xử lý hoặc tham khảo mặt hàng HGT trong danh mục.'),
'ca-ro-phi':('Cá rô phi — thông tin cho đơn hàng','Nêu rõ dạng nguyên con hoặc yêu cầu xử lý, kích cỡ và mục đích sử dụng. MAI KỲ HÀ tiếp nhận thông tin để trao đổi khả năng đáp ứng, đóng gói và lịch giao theo nhu cầu.'),
'ca-ngan-duoi-vang':('Trao đổi mặt hàng cá ngân đuôi vàng','Tham khảo ảnh thực tế và gửi yêu cầu theo tên mặt hàng trong danh mục. Hãy ghi rõ đơn vị kích cỡ, khối lượng, đóng gói và điểm giao dự kiến để thuận tiện đối chiếu.'),
'ca-ngu-vay-vang':('Cá ngừ vây vàng — xác định rõ nhu cầu','Ghi rõ cá ngừ vây vàng để phân biệt với cá ngừ ồ trong danh mục. Dạng xử lý, kích cỡ, yêu cầu chất lượng và quy cách đóng gói được trao đổi theo mục đích sử dụng của đối tác.')}

def finish(path,title,body,products,icon):
 if path=='/':return body
 # Add intermediate levels to breadcrumbs on deep pages.
 for parent,label in [('/san-pham/','Sản phẩm'),('/kien-thuc/','Kiến thức'),('/hoat-dong/','Hoạt động')]:
  if path.startswith(parent) and path!=parent:
   body=body.replace('<span>/</span><span aria-current="page">',f'<span>/</span><a href="{parent}">{label}</a><span>/</span><span aria-current="page">',1)
 if path.startswith('/san-pham/') and path!='/san-pham/':
  slug=path.strip('/').split('/')[-1];p=next(p for p in products if p['slug']==slug);heading,copy=product_focus[slug]
  body=body.replace('<h2>Thông tin hỏi hàng</h2>',f'<p class="eyebrow">{escape(p["en"])}</p><h2>{heading}</h2><p>{copy}</p><h3>Thông tin cần xác nhận</h3>',1)
  body=body.replace('<th scope="row">Sản phẩm</th>', '<th scope="row">Tên mặt hàng</th>')
  body=body.replace('Cho chúng tôi biết quy cách, khối lượng, địa điểm giao và thời gian cần hàng để trao đổi cụ thể.','Chọn “Hỏi về sản phẩm này” để mở biểu mẫu có sẵn tên mặt hàng. Bạn chỉ cần bổ sung quy cách và nhu cầu giao hàng.')
  body+=f'<section class="cta"><div class="wrap"><div><p class="eyebrow">KẾT NỐI ĐẠI DƯƠNG, PHỦ SÓNG TOÀN CẦU</p><h2>Bạn cần thêm thông tin về {p["name"].lower()}?</h2><p>Gửi yêu cầu hoặc gọi 0235 356 5568 để trao đổi.</p></div><a class="button" href="/lien-he/?san-pham={slug}">Hỏi về sản phẩm này</a></div></section>'
 if path.startswith('/kien-thuc/') and path!='/kien-thuc/':
  start=body.index('<article class="section prose wrap">');end=body.index('</article>',start)
  article=body[start:end];headings=re.findall(r'<h2>(.*?)</h2>',article)
  for i,h in enumerate(headings,1):article=article.replace(f'<h2>{h}</h2>',f'<h2 id="muc-{i}">{h}</h2>',1)
  toc='<div class="article-contents"><p class="eyebrow">NỘI DUNG BÀI VIẾT</p><ol>'+''.join(f'<li><a href="#muc-{i}">{h}</a></li>' for i,h in enumerate(headings,1))+'</ol></div>'
  article=article.replace('<article class="section prose wrap">','<article class="section prose wrap">'+toc)
  body=body[:start]+article+body[end:]
 if path=='/lien-he/':
  start=body.index('<aside>');end=body.index('</aside>',start)+len('</aside>')
  aside=f'''<aside class="contact-sidebar"><p class="eyebrow">KẾT NỐI CÙNG CHÚNG TÔI</p><h2>MAI KỲ HÀ</h2><p>Thương mại và xuất nhập khẩu thủy sản</p><div class="contact-method"><span class="contact-icon">{icon('pin')}</span><div><h3>Địa chỉ công ty</h3><p>452 Phạm Văn Đồng, Xã Núi Thành,<br>Thành phố Đà Nẵng</p></div></div><a class="contact-method" href="tel:+842353565568"><span class="contact-icon">{icon('phone')}</span><div><h3>Gọi trao đổi</h3><span>0235 356 5568</span></div></a><a class="contact-method" href="mailto:maikyhaseafood01@gmail.com"><span class="contact-icon">{icon('mail')}</span><div><h3>Gửi email</h3><span>maikyhaseafood01@gmail.com</span></div></a><div class="editorial-note">Bạn có ảnh tham khảo hoặc tài liệu quy cách? Hãy đính kèm trong email sau khi mở nội dung yêu cầu.</div></aside>'''
  body=body[:start]+aside+body[end:]
 if path=='/nang-luc/':
  body=body.replace('<div class="wrap"><div class="section-heading"><h2>Xử lý', '<div class="wrap"><p class="eyebrow">CÔNG ĐOẠN 01</p><div class="section-heading"><h2>Xử lý',1)
  body=body.replace('<div class="wrap"><div class="section-heading"><h2>Lưu kho', '<div class="wrap"><p class="eyebrow">CÔNG ĐOẠN 02</p><div class="section-heading"><h2>Lưu kho',1)
  body=body.replace('<div class="wrap"><div class="section-heading"><h2>Đóng hàng', '<div class="wrap"><p class="eyebrow">CÔNG ĐOẠN 03</p><div class="section-heading"><h2>Đóng hàng',1)
 return body
