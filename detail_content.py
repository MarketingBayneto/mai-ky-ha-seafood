from html import escape

def section(kicker,title,copy,items,cls=''):
 cards=''.join(f'<article class="detail-tile"><span class="detail-index">{i:02}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(items,1))
 return f'<section class="section {cls}"><div class="wrap"><p class="eyebrow">{kicker}</p><div class="section-heading"><h2>{title}</h2><p>{copy}</p></div><div class="detail-tiles">{cards}</div></div></section>'

def faq(items):
 return '<section class="section pale"><div class="wrap faq-wrap"><div><p class="eyebrow">GIẢI ĐÁP</p><h2>Thông tin trước khi hợp tác</h2></div><div>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)+'</div></div></section>'

def image_story(src,alt,kicker,title,copy,href,label):
 return f'<section class="section deep-section"><div class="wrap split"><img class="editorial-photo" src="{src}" alt="{alt}" loading="lazy"><div><p class="eyebrow">{kicker}</p><h2>{title}</h2><p>{copy}</p><a class="button" href="{href}">{label}</a></div></div></section>'

common_faq=[('Có thể hỏi hàng theo quy cách riêng không?','Bạn có thể gửi dạng xử lý, kích cỡ, khối lượng mỗi kiện và yêu cầu nhãn. MAI KỲ HÀ sẽ trao đổi khả năng đáp ứng cho từng mặt hàng, từng lô hàng.'),('Làm thế nào để nhận thông tin giá và lịch giao?','Gửi mặt hàng, quy cách, khối lượng, điểm giao và thời gian cần hàng. Giá và lịch thực hiện được trao đổi theo nhu cầu cụ thể, sau khi làm rõ thông tin.'),('Cần trao đổi gì về hồ sơ và chất lượng?','Nêu thị trường giao dịch, tiêu chí chất lượng và danh mục hồ sơ bên mua yêu cầu. Các thông tin về nguồn gốc, bảo quản và chứng từ cần được xác nhận cho lô hàng trước khi thống nhất giao dịch.')]

extras={
'/gioi-thieu/':section('ĐỊNH HƯỚNG HỢP TÁC','Kết nối đại dương,<br>phủ sóng toàn cầu','Slogan thể hiện khát vọng đưa thủy sản Việt Nam đến gần hơn với các thị trường quốc tế. MAI KỲ HÀ theo đuổi định hướng đó bằng sự chú trọng vào chất lượng sản phẩm, thông tin rõ ràng và quan hệ hợp tác lâu dài.',[
('Tập trung vào thủy sản','Danh mục cá và mực phục vụ nhu cầu thương mại, phân phối và nguyên liệu. Mặt hàng, dạng xử lý và đóng gói được trao đổi theo đơn hàng.'),('Chú trọng chất lượng','Độ tươi, cảm quan và điều kiện bảo quản là những nội dung cần làm rõ cùng quy cách. Hình ảnh thực tế giúp đối tác có thêm cơ sở trao đổi.'),('Kết nối lâu dài','Thống nhất đầu mối làm việc, nhu cầu và các mốc triển khai để phối hợp xuyên suốt quá trình giao dịch.')])+image_story('/assets/hoi-cho-1.webp','Gặp gỡ đối tác tại triển lãm','KẾT NỐI DOANH NGHIỆP','Mở rộng cơ hội từ những cuộc gặp trực tiếp','Các hoạt động hội chợ là dịp giới thiệu sản phẩm, tìm hiểu nhu cầu thị trường và trao đổi cơ hội hợp tác với doanh nghiệp trong ngành.','/hoat-dong/hoi-cho/','Xem hình ảnh hội chợ'),
'/san-pham/':section('LỰA CHỌN PHÙ HỢP','Từ tên mặt hàng<br>đến quy cách bạn cần','Ảnh trong danh mục là ảnh thực tế do công ty cung cấp. Quy cách và khả năng cung ứng được xác nhận khi hỏi hàng.',[
('Chọn dòng sản phẩm','Sử dụng bộ lọc để tìm nhóm cá ngừ, cá nục – bạc má – cá sòng, các loại cá khác hoặc mực.'),('Xem hình ảnh chi tiết','Mở từng sản phẩm để xem thêm ảnh, đối chiếu dạng hàng và chuẩn bị câu hỏi cụ thể.'),('Gửi yêu cầu rõ ràng','Nêu kích cỡ, cách xử lý, đóng gói và khối lượng mong muốn để việc trao đổi sát nhu cầu hơn.')],'pale')+faq(common_faq[:2]),
'/thuong-mai-xnk/':image_story('/assets/dong-hang-1.webp','Chuẩn bị lô hàng thủy sản','GIAO DỊCH THEO NHU CẦU','Một phương án phù hợp bắt đầu từ thông tin đầy đủ','Dù tìm mua một mặt hàng cụ thể hay giới thiệu nguồn cung, đối tác có thể gửi yêu cầu để cùng làm rõ sản phẩm, điều kiện giao nhận và phạm vi phối hợp.','/lien-he/','Trao đổi phương án')+section('NỘI DUNG CẦN THỐNG NHẤT','Rõ từng yêu cầu<br>trước khi triển khai','Các nội dung dưới đây được trao đổi cho từng giao dịch, theo mặt hàng và thị trường dự kiến.',[
('Hàng hóa & chất lượng','Tên hàng, dạng xử lý, kích cỡ, yêu cầu cảm quan, bảo quản và tiêu chí nghiệm thu.'),('Bao bì & hồ sơ','Quy cách thùng, khối lượng, thông tin nhãn, nguồn gốc và các chứng từ đối tác yêu cầu.'),('Giao nhận & thương mại','Khối lượng, giá, phạm vi chi phí, lịch giao, địa điểm, phương thức thanh toán và trách nhiệm mỗi bên.')])+faq(common_faq),
'/nang-luc/':section('CHẤT LƯỢNG XUYÊN SUỐT','Chú trọng độ tươi<br>qua từng công đoạn','Chất lượng thành phẩm gắn liền với cách xử lý, điều kiện lưu giữ và phối hợp giao nhận. Yêu cầu cụ thể được làm rõ theo dạng hàng.',[
('Quy cách xử lý','Làm rõ dạng sản phẩm, phân loại, kích cỡ và cách đóng gói phù hợp với mục đích sử dụng của đối tác.'),('Điều kiện bảo quản','Trao đổi điều kiện lưu giữ, yêu cầu nhiệt độ và thông tin theo dõi phù hợp với sản phẩm và lô hàng.'),('Kiểm tra trước giao','Đối chiếu mặt hàng, số kiện, bao bì, nhãn và hồ sơ đã thống nhất trước khi phối hợp giao nhận.')],'pale'),
'/hoat-dong/':image_story('/assets/ca-ngu-o-1.webp','Hình ảnh sản phẩm cá ngừ thực tế','TỪ SẢN PHẨM ĐẾN ĐỐI TÁC','Nhìn gần hơn vào hàng hóa','Khám phá hình ảnh từng dòng sản phẩm để trao đổi nhu cầu bằng những thông tin cụ thể: mặt hàng, dạng xử lý và quy cách mong muốn.','/san-pham/','Khám phá sản phẩm')+section('KẾT NỐI & PHỐI HỢP','Những nội dung trong mỗi cuộc trao đổi','Hoạt động gặp gỡ giúp hai bên hiểu nhau hơn trước khi đi vào phương án hợp tác.',[('Giới thiệu sản phẩm','Chia sẻ danh mục và hình ảnh hàng hóa phù hợp với nhu cầu quan tâm.'),('Tìm hiểu thị trường','Trao đổi yêu cầu về dạng hàng, đóng gói và nhu cầu sử dụng của đối tác.'),('Tiếp nối hợp tác','Ghi nhận thông tin cần làm rõ và kết nối đầu mối để trao đổi chi tiết.')]),
'/hoat-dong/hoi-cho/':section('TRAO ĐỔI TẠI TRIỂN LÃM','Kết nối qua nhu cầu thực tế','Mỗi cuộc gặp mở ra cơ hội tìm hiểu sản phẩm và cách làm việc của các bên.',[('Giới thiệu mặt hàng','Trao đổi danh mục thủy sản và những dòng hàng đối tác đang quan tâm.'),('Lắng nghe yêu cầu','Tìm hiểu quy cách, mục đích sử dụng và nhu cầu thị trường.'),('Kết nối sau hội chợ','Tiếp tục trao đổi thông tin và làm rõ khả năng phối hợp cho các yêu cầu cụ thể.')],'pale'),
'/kien-thuc/':faq([('Chưa biết chính xác quy cách, tôi có thể liên hệ không?','Có. Hãy gửi tên mặt hàng, mục đích sử dụng hoặc ảnh tham khảo và khối lượng dự kiến. Những thông tin còn thiếu có thể tiếp tục làm rõ trong quá trình trao đổi.'),('Hình ảnh có thay thế được thông tin quy cách không?','Hình ảnh giúp nhận diện sản phẩm nhưng không thể hiện đầy đủ kích cỡ, khối lượng, dạng xử lý hay điều kiện bảo quản. Cần xác nhận các nội dung này bằng thông tin cụ thể cho đơn hàng.')]),
'/lien-he/':section('CHUẨN BỊ TRƯỚC KHI LIÊN HỆ','Để cuộc trao đổi<br>đi thẳng vào nhu cầu','Bạn có thể gửi những thông tin đã có; các chi tiết còn lại sẽ được làm rõ trong quá trình trao đổi.',[('Bạn cần mặt hàng nào?','Tên cá hoặc mực, dạng xử lý và kích cỡ mong muốn. Nếu chưa rõ tên, có thể mô tả hoặc gửi ảnh qua email.'),('Bạn dự kiến đặt bao nhiêu?','Khối lượng, đơn vị tính, nhu cầu một lần hay định kỳ và thời gian cần hàng.'),('Hàng sẽ giao ở đâu?','Địa điểm, thị trường dự kiến cùng các yêu cầu đóng gói, nhãn và hồ sơ cần trao đổi.')],'pale')+faq(common_faq[:2])
}

images={'/gioi-thieu/':('hoi-cho-0.webp','Hoạt động kết nối của MAI KỲ HÀ'),'/san-pham/':('ca-ngu-o-0.webp','Sản phẩm cá ngừ thực tế'),'/thuong-mai-xnk/':('dong-hang-0.webp','Chuẩn bị giao hàng thủy sản'),'/nang-luc/':('xuong-0.webp','Khu vực xử lý sản phẩm'),'/hoat-dong/':('hoi-cho-0.webp','Gặp gỡ tại triển lãm'),'/hoat-dong/hoi-cho/':('hoi-cho-4.webp','Hoạt động tại hội chợ'),'/kien-thuc/':('xuong-3.webp','Khu vực xử lý sản phẩm'),'/lien-he/':('kho-0.webp','Thành phẩm của công ty')}
article_notes={
'hoi-hang':('Mẫu thông tin hỏi hàng','Sản phẩm: … / Dạng xử lý: … / Kích cỡ và đơn vị: … / Khối lượng: … / Đóng gói: … / Điểm giao: … / Thời gian cần hàng: … / Hồ sơ yêu cầu: …','Nếu chưa xác định được một thông tin, hãy ghi “cần trao đổi thêm” thay vì bỏ trống hoặc tự ước lượng.'),
'quy-cach':('Kiểm tra cách ghi đơn vị','Phân biệt rõ kích cỡ theo gram/con, con/kg hoặc cách phân cỡ khác; khối lượng theo kg hoặc tấn; đóng gói theo kg/kiện. Nếu có yêu cầu về khối lượng tịnh và khối lượng cả bao bì, hãy ghi riêng từng mục.','Mọi ví dụ đơn vị chỉ giúp mô tả yêu cầu, không phải quy cách cung ứng mặc định của MAI KỲ HÀ.'),
'dieu-kien-giao-dich':('Đối chiếu trước khi xác nhận','Kiểm tra bản trao đổi cuối cùng có đủ: tên hàng, quy cách, khối lượng, giá và phạm vi chi phí, thanh toán, điểm giao, lịch thực hiện, tiêu chí nghiệm thu và hồ sơ đi kèm.','Những nội dung chưa thống nhất nên được làm rõ bằng văn bản với đầu mối phụ trách trước khi triển khai.')}

def enrich(path,title,body,products):
 if path=='/':return body
 crumb=f'<nav class="breadcrumbs wrap" aria-label="Đường dẫn"><a href="/">Trang chủ</a><span>/</span><span aria-current="page">{escape(title)}</span></nav>'
 if path in images:
  src,alt=images[path]
  body=body.replace('<section class="page-intro sea">',f'<section class="page-intro sea illustrated-intro"><img class="intro-photo" src="/assets/{src}" alt="{alt}" loading="eager">',1)
 extra=extras.get(path,'')
 if path.startswith('/san-pham/') and path!='/san-pham/':
  item=next((p for p in products if path=='/san-pham/'+p['slug']+'/'),None)
  if item:
   related=[p for p in products if p['slug']!=item['slug'] and p['group']==item['group']][:3]
   if not related:related=[p for p in products if p['slug']!=item['slug']][:3]
   extra=section('CHẤT LƯỢNG & QUY CÁCH','Làm rõ yêu cầu cho '+item['name'].lower(),'Hình ảnh là cơ sở tham khảo ban đầu. Thông tin của lô hàng được xác nhận khi trao đổi.',[('Dạng hàng','Nêu yêu cầu nguyên con hoặc xử lý, kích cỡ và đơn vị phân cỡ bạn cần.'),('Bảo quản & đóng gói','Trao đổi điều kiện bảo quản, khối lượng mỗi kiện và yêu cầu nhãn phù hợp.'),('Thông tin lô hàng','Xác nhận khối lượng, nguồn gốc, hồ sơ và lịch giao dự kiến trước khi thống nhất.')],'pale')
   extra+='<section class="section"><div class="wrap"><p class="eyebrow">KHÁM PHÁ THÊM</p><h2>Các sản phẩm liên quan</h2><div class="three">'+''.join(f'<a class="product-card" href="/san-pham/{p["slug"]}/"><img src="{p["images"][0]}" alt="{p["name"]}" loading="lazy"><div><h3>{p["name"]}</h3><p>{p["en"]}</p><span>Xem chi tiết</span></div></a>' for p in related)+'</div></div></section>'
 if path.startswith('/kien-thuc/') and path!='/kien-thuc/':
  slug=path.strip('/').split('/')[-1]
  if slug in article_notes:
   h,p,note=article_notes[slug]
   extra=f'<section class="section pale"><div class="wrap prose"><p class="eyebrow">ÁP DỤNG KHI HỎI HÀNG</p><h2>{h}</h2><p>{p}</p><div class="editorial-note">{note}</div><a class="text-link" href="/kien-thuc/">Xem các hướng dẫn khác</a></div></section>'
 if '<section class="cta">' in body:body=body.replace('<section class="cta">',extra+'<section class="cta">',1)
 else:body+=extra
 return crumb+body
