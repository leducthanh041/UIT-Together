# Nguồn ảnh cho tạp chí và hội nghị

Kiểm tra ngày 2026-10-10. Danh mục `src/data/venues.json` có 42 venue. Tất cả trường `image` hiện để rỗng vì chưa có ảnh bìa hoặc logo venue được kiểm chứng trong bộ asset đang dùng. Các đường dẫn dưới đây là tên file đề xuất để người dùng tải ảnh về; chúng chưa tồn tại. Không dùng URL ảnh suy đoán hoặc hotlink trong giao diện.

## Ba ảnh legacy không phải ảnh bìa

Đã mở và kiểm tra trực tiếp ba file có tên dễ gây nhầm:

- `/assets/images/papers/prlt.jpg`: sơ đồ kiến trúc mô hình human-object interaction, có chú thích Figure 1.
- `/assets/images/papers/ijdar.jpg`: biểu đồ benchmark các bộ phát hiện đối tượng.
- `/assets/images/papers/mdpi.jpg`: bảng Comparison of related works.

Giữ nguyên `image` trong từng publication vì đó là hình minh họa bài báo. Không đưa ba file này vào `venues.json` như ảnh bìa. Bộ `legacy/jekyll/_site` còn ảnh bìa thuộc website mẫu cũ, không thuộc venue của 150 bản ghi hiện tại.

## Nguồn chính thức đã tra cứu

| Venue | Nguồn chính thức | Kết quả kiểm tra và ảnh phù hợp | File local đề xuất |
| --- | --- | --- | --- |
| IEEE Access | [IEEE Access](https://ieeeaccess.ieee.org/) | Đọc được trang chính thức. Đây là online-only journal; dùng nhận diện IEEE Access trên trang nhà xuất bản hoặc ảnh bìa do IEEE cung cấp. Không dùng hình của một bài báo làm bìa. Chưa xác định URL file cover riêng. | `src/assets/images/venues/ieee-access.webp` |
| Pattern Recognition Letters | [ScienceDirect journal](https://www.sciencedirect.com/journal/pattern-recognition-letters) | Trang chính thức trả 403 trong lượt kiểm tra. Người dùng có thể mở bằng trình duyệt và lưu ảnh bìa ở mục journal/latest issue. Chưa kiểm chứng URL ảnh trực tiếp. | `src/assets/images/venues/pattern-recognition-letters.webp` |
| IJDAR | [Springer journal](https://link.springer.com/journal/10032) | Đọc được trang chính thức, liên kết Image ngay trước Latest issue trỏ tới [bìa volume 29, issue 2](https://media.springernature.com/w68/springer-static/cover/journal/10032/29/2.jpg?as=webp). Đây là URL lấy từ chính trang Springer, nhưng tải ảnh qua công cụ bị Cache miss; chưa kiểm tra ảnh tải về. Có thể dùng bìa năm của bài báo nếu muốn. | `src/assets/images/venues/ijdar.webp` |
| Journal of Imaging | [MDPI journal](https://www.mdpi.com/journal/jimaging) và [Aims & Scope](https://www.mdpi.com/journal/jimaging/about) | Search trả nội dung chính thức; mở trực tiếp bị 429. Lấy bìa/logo Journal of Imaging từ trang journal hoặc issue, không lấy bảng `mdpi.jpg` của bài báo. Chưa kiểm chứng URL ảnh trực tiếp. | `src/assets/images/venues/journal-of-imaging.webp` |
| ACM Computing Surveys | [ACM Digital Library](https://dl.acm.org/journal/csur) | Trang chính thức trả 403. Lấy bìa hoặc nhận diện CSUR từ journal/issue trên ACM. Chưa kiểm chứng URL ảnh trực tiếp. | `src/assets/images/venues/acm-computing-surveys.webp` |
| KSE | [KSE 2023](https://kse2023.kse-conferences.org/) | Đọc được trang chính thức. Dùng logo KSE hoặc cover proceedings đúng năm; không dùng logo IEEE thay cho tên hội nghị. Chưa kiểm chứng URL ảnh trực tiếp. | `src/assets/images/venues/kse.webp` |
| FAIR | [FAIR 2023](https://fair.conf.vn/2023/) và [CFP chính thức](https://fair.conf.vn/2023/images/CFP01.pdf) | Đọc được trang hội nghị. Dùng banner/nhận diện FAIR hoặc bìa kỷ yếu; ảnh mang năm 2023 không tự đại diện mọi năm nếu có nội dung ngày/địa điểm. Chưa kiểm chứng URL ảnh trực tiếp. | `src/assets/images/venues/fair.webp` |
| REV-ECIT | [REV-ECIT 2023](https://2023.rev-ecit.vn/) | Search trả trang chính thức với mục kỷ yếu và thư mời; open không lấy được trang trong lượt này. Dùng logo hội nghị hoặc cover proceedings đúng năm. Chưa kiểm chứng URL ảnh trực tiếp. | `src/assets/images/venues/rev-ecit.webp` |

## Toàn bộ venue và tên file dự kiến

Các venue có nguồn rỗng chưa được xác minh website chính thức trong lượt này. Tên venue được chuẩn hóa từ citation gốc, không đồng nghĩa đã xác minh logo, ảnh bìa hay thông tin xuất bản trên web. Không gán một website không rõ nguồn chỉ để lấp trường trống.

| Slug | Tên | Loại | File local đề xuất | Nguồn chính thức / trạng thái |
| --- | --- | --- | --- | --- |
| `acm-computing-surveys` | ACM Computing Surveys | journal | `src/assets/images/venues/acm-computing-surveys.webp` | [Trang venue](https://dl.acm.org/journal/csur) |
| `caip` | International Conference on Computer Analysis of Images and Patterns (CAIP) | conference | `src/assets/images/venues/caip.webp` | Chưa xác minh; để trống `source_url` |
| `can-tho-university-journal-of-science` | Can Tho University Journal of Science | journal | `src/assets/images/venues/can-tho-university-journal-of-science.webp` | Chưa xác minh; để trống `source_url` |
| `cita` | Conference on Information Technology and its Applications (CITA) | conference | `src/assets/images/venues/cita.webp` | Chưa xác minh; để trống `source_url` |
| `csae` | Computer Science and Automation Engineering | conference | `src/assets/images/venues/csae.webp` | Chưa xác minh; để trống `source_url` |
| `electronics` | Electronics | journal | `src/assets/images/venues/electronics.webp` | [Trang venue](https://www.mdpi.com/journal/electronics) |
| `fair` | National Conference on Fundamental and Applied Information Technology Research (FAIR) | conference | `src/assets/images/venues/fair.webp` | [Trang venue](https://fair.conf.vn/2023/) |
| `icarcv` | International Conference on Control, Automation, Robotics and Vision (ICARCV) | conference | `src/assets/images/venues/icarcv.webp` | Chưa xác minh; để trống `source_url` |
| `iccci` | International Conference on Computer and Computational Intelligence | conference | `src/assets/images/venues/iccci.webp` | Chưa xác minh; để trống `source_url` |
| `icce` | International Conference on Communications and Electronics (ICCE) | conference | `src/assets/images/venues/icce.webp` | Chưa xác minh; để trống `source_url` |
| `icinar` | International Asia Conference on Informatics in Control, Automation and Robotics | conference | `src/assets/images/venues/icinar.webp` | Chưa xác minh; để trống `source_url` |
| `icsip` | International Conference on Signal and Image Processing (ICSIP) | conference | `src/assets/images/venues/icsip.webp` | Chưa xác minh; để trống `source_url` |
| `ieee-access` | IEEE Access | journal | `src/assets/images/venues/ieee-access.webp` | [Trang venue](https://ieeeaccess.ieee.org/) |
| `ieee-jstars` | IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing | journal | `src/assets/images/venues/ieee-jstars.webp` | Chưa xác minh; để trống `source_url` |
| `ijacsa` | International Journal of Advanced Computer Science and Applications (IJACSA) | journal | `src/assets/images/venues/ijacsa.webp` | Chưa xác minh; để trống `source_url` |
| `ijdar` | International Journal on Document Analysis and Recognition (IJDAR) | journal | `src/assets/images/venues/ijdar.webp` | [Trang venue](https://link.springer.com/journal/10032) |
| `imcom` | International Conference on Ubiquitous Information Management and Communication (IMCOM) | conference | `src/assets/images/venues/imcom.webp` | Chưa xác minh; để trống `source_url` |
| `international-journal-of-computer-science-issues` | International Journal of Computer Science Issues | journal | `src/assets/images/venues/international-journal-of-computer-science-issues.webp` | Chưa xác minh; để trống `source_url` |
| `international-journal-on-computer-science-and-engineering` | International Journal on Computer Science and Engineering | journal | `src/assets/images/venues/international-journal-on-computer-science-and-engineering.webp` | Chưa xác minh; để trống `source_url` |
| `journal-of-computer-science-and-cybernetics` | Journal of Computer Science and Cybernetics | journal | `src/assets/images/venues/journal-of-computer-science-and-cybernetics.webp` | Chưa xác minh; để trống `source_url` |
| `journal-of-imaging` | Journal of Imaging | journal | `src/assets/images/venues/journal-of-imaging.webp` | [Trang venue](https://www.mdpi.com/journal/jimaging) |
| `journal-of-science-unresolved` | Journal of Science | journal | `src/assets/images/venues/journal-of-science-unresolved.webp` | Citation chỉ ghi Journal of Science; chưa xác định nhà xuất bản |
| `journal-of-technical-education-science` | Journal of Technical Education Science | journal | `src/assets/images/venues/journal-of-technical-education-science.webp` | Chưa xác minh; để trống `source_url` |
| `journal-of-visual-communication-and-image-representation` | Journal of Visual Communication and Image Representation | journal | `src/assets/images/venues/journal-of-visual-communication-and-image-representation.webp` | Chưa xác minh; để trống `source_url` |
| `jstic` | Journal of Science and Technology on Information and Communications | journal | `src/assets/images/venues/jstic.webp` | Chưa xác minh; để trống `source_url` |
| `kicss` | International Conference on Knowledge, Information and Creativity Support Systems (KICSS) | conference | `src/assets/images/venues/kicss.webp` | Chưa xác minh; để trống `source_url` |
| `kse` | International Conference on Knowledge and Systems Engineering (KSE) | conference | `src/assets/images/venues/kse.webp` | [Trang venue](https://kse2023.kse-conferences.org/) |
| `mapr` | International Conference on Multimedia Analysis and Pattern Recognition (MAPR) | conference | `src/assets/images/venues/mapr.webp` | Chưa xác minh; để trống `source_url` |
| `mita` | International Conference on Multimedia Information Technology and Applications (MITA) | conference | `src/assets/images/venues/mita.webp` | Chưa xác minh; để trống `source_url` |
| `mmm` | International Conference on Multimedia Modeling (MMM) | conference | `src/assets/images/venues/mmm.webp` | Chưa xác minh; để trống `source_url` |
| `multimedia-tools-and-applications` | Multimedia Tools and Applications | journal | `src/assets/images/venues/multimedia-tools-and-applications.webp` | Chưa xác minh; để trống `source_url` |
| `nics` | NAFOSTED Conference on Information and Computer Science (NICS) | conference | `src/assets/images/venues/nics.webp` | Chưa xác minh; để trống `source_url` |
| `pattern-recognition-letters` | Pattern Recognition Letters | journal | `src/assets/images/venues/pattern-recognition-letters.webp` | [Trang venue](https://www.sciencedirect.com/journal/pattern-recognition-letters) |
| `rev-ecit` | National Conference on Electronics, Communications and Information Technology (REV-ECIT) | conference | `src/assets/images/venues/rev-ecit.webp` | [Trang venue](https://2023.rev-ecit.vn/) |
| `rivf` | RIVF International Conference on Computing and Communication Technologies | conference | `src/assets/images/venues/rivf.webp` | Chưa xác minh; để trống `source_url` |
| `saigon-university-journal` | Tạp chí Đại Học Sài Gòn | journal | `src/assets/images/venues/saigon-university-journal.webp` | Chưa xác minh; để trống `source_url` |
| `selected-ict-problems` | National Symposium of Selected ICT Problems | conference | `src/assets/images/venues/selected-ict-problems.webp` | Chưa xác minh; để trống `source_url` |
| `socpar` | International Conference of Soft Computing and Pattern Recognition | conference | `src/assets/images/venues/socpar.webp` | Chưa xác minh; để trống `source_url` |
| `soict` | International Symposium on Information and Communication Technology (SOICT) | conference | `src/assets/images/venues/soict.webp` | Chưa xác minh; để trống `source_url` |
| `tnu-journal-of-science-and-technology` | TNU Journal of Science and Technology | journal | `src/assets/images/venues/tnu-journal-of-science-and-technology.webp` | Chưa xác minh; để trống `source_url` |
| `vietnam-journal-of-computer-science` | Vietnam Journal of Computer Science | journal | `src/assets/images/venues/vietnam-journal-of-computer-science.webp` | Chưa xác minh; để trống `source_url` |
| `vietnam-journal-of-science-and-technology` | Vietnam Journal of Science and Technology | journal | `src/assets/images/venues/vietnam-journal-of-science-and-technology.webp` | Chưa xác minh; để trống `source_url` |

Sau khi tải và kiểm tra ảnh thực tế, đặt file tại đường dẫn tương ứng. Build tự nhận `<slug>.webp` (hoặc png/jpg/jpeg/svg) khi `venues[slug].image` rỗng; cũng có thể khai báo `image` thành `/assets/images/venues/<slug>.webp` rõ ràng. Chỉ trỏ tới file có thật. Không thay đổi `publication.image` để thay minh họa nghiên cứu bằng bìa venue.

## Quy tắc và kết quả chuẩn hóa metadata

- Giữ nguyên 150 ID, citation, authors, links, year, layouts và image. Không thay đổi route hoặc các tham chiếu publication trong page.
- Tiêu đề lấy từ title hiện có, phần trong dấu ngoặc kép của citation hoặc danh sách chuỗi tiêu đề đã đối chiếu trực tiếp trong citation legacy. Chuẩn hóa khoảng trắng và bỏ dấu chấm phân cách cuối title; bỏ ghi chú `(accepted)` khỏi title nhưng giữ citation nguyên.
- `display_title` dùng title đáng tin cậy; chỉ dùng citation làm fallback khi không tách được title. Lượt này tách được title cho cả 150 bản ghi, nên không có citation fallback.
- Phân loại theo venue thực tế, kể cả bài journal nằm trong nhóm conference của trang legacy. Có 56 bản ghi journal, 94 conference, 0 unknown. Đây là số bản ghi gốc, gồm bản ghi lặp; không phải 150 công trình riêng biệt.
- DOI chỉ lấy từ DOI URL, đường dẫn publisher chứa DOI đầy đủ (Springer article/chapter, ACM doi), hoặc hai nguồn đã kiểm chứng trong cùng task. Không suy DOI từ IEEE document ID, ScienceDirect PII, mã arXiv hoặc DOI của venue.
- Truyền DOI giữa bản ghi có cùng title chính xác sau chuẩn hóa và cùng venue. DOI đang có không bị ghi đè. Có 20 bản ghi chứa DOI, tương ứng 9 DOI khác nhau; 130 bản ghi còn để DOI rỗng.
- DOI bổ sung cho PR Letters: [publisher DOI](https://doi.org/10.1016/j.patrec.2023.09.013), được agent chính xác minh trong cùng task; công cụ của subagent mở lại trả 403. DOI bổ sung cho Vietnamese Document Analysis: [bản lưu tại University of Dayton](https://ecommons.udayton.edu/cps_fac_pub/193/), đọc được trường DOI `10.1109/ACCESS.2022.3211069`.
- `metadata_source` ghi cách tách title; `doi_source` lưu URL nguồn DOI. Các trường authors trống trước đó vẫn giữ trống; citation gốc còn đủ nội dung tác giả.

### Ba bản ghi cần kiểm tra metadata

| ID | Vấn đề |
| --- | --- |
| `937a0e940065` | Citation ghi accepted nhưng không có năm công bố |
| `d6ea3ed53089` | Citation ghi accepted nhưng không có năm công bố |
| `7a55e6bd14af` | Tên Journal of Science quá chung, chưa xác định được journal cụ thể |

Các biến thể title như VinaFood21 có/không có tiền tố, CDeRSNet với Document/Documents hoặc tiêu đề tiếng Việt khác nhau được giữ theo nguồn gốc. Không tự sửa thành cùng một công trình; nếu cần hợp nhất sâu hơn phải đối chiếu publisher/DOI.
