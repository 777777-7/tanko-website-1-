# -*- coding: utf-8 -*-
"""
Bahasa Malaysia category landing pages.

These are the commercial entry points for Malay-language search — a buyer
searching "beli meja kerja industri" or "pembekal kabinet alat bengkel" lands
ready to enquire, not to read a guide. The Bahasa guides in guides_bm*.py
serve informational intent; these serve transactional intent.

Each entry pairs with an existing English category via `en_slug`, which drives
reciprocal hreflang. Copy is original Bahasa written for this audience, not a
translation of the English intro — Google detects and suppresses machine
translation, and a half-translated page competes with its own English
counterpart.

FAQs feed FAQPage schema, which materially improves inclusion in AI Overviews
and answer engines.
"""

CATEGORIES_BM = [
    {
        "slug": "meja-kerja",
        "en_slug": "workbench",
        "name": "Meja Kerja Industri",
        "h1": "Meja Kerja Industri Malaysia — Pengedar Eksklusif Tanko",
        "meta": "Meja kerja industri Tanko untuk kilang dan bengkel di Malaysia. Permukaan getah, laminate, kayu dan keluli tahan karat. Stok Selangor, harga Ringgit.",
        "intro": (
            "Meja kerja industri Tanko untuk kilang, bengkel dan barisan pemasangan di seluruh Malaysia. "
            "Rangkaian kami merangkumi meja tugas sederhana untuk kerja pemasangan dan pemeriksaan, "
            "sehingga meja tugas berat untuk fabrikasi, kimpalan dan penyelenggaraan."
        ),
        "body": (
            "<p>Pilihan permukaan menentukan berapa lama meja bertahan. Permukaan getah menyerap hentakan "
            "dan sesuai untuk kerja mekanikal. Laminate bersih dan senyap untuk pemasangan dan elektronik. "
            "Keluli tahan karat untuk industri makanan, farmaseutikal, makmal dan kawasan basah. Permukaan "
            "keluli menahan penderaan berat, haba dan beban tinggi.</p>"
            "<p>Kadar tugas adalah keputusan kedua yang paling penting. Pilih berdasarkan barang paling berat "
            "yang akan diletakkan di atas meja, bukan purata — dan ambil kira sama ada beban itu tertumpu di "
            "satu titik atau tersebar merata. Kadar dalam katalog biasanya merujuk kepada beban teragih sekata.</p>"
            "<p>Semua meja boleh dikonfigurasikan dengan laci, papan berlubang belakang, rak atas, lampu tugas "
            "dan rel kuasa. Untuk barisan yang mungkin berubah dalam dua hingga tiga tahun, "
            "<a href=\"/stesen-kerja/\">stesen kerja modular</a> mungkin lebih menjimatkan kerana rangka yang "
            "sama menyokong konfigurasi baharu.</p>"
        ),
        "faqs": [
            {"q": "Berapa harga meja kerja industri di Malaysia?",
             "a": "Harga bergantung pada kadar tugas, bahan permukaan, bilangan laci dan aksesori. Sebagai panduan, meja kerja asas bermula sekitar RM900 dan meja tugas berat dengan konfigurasi penuh boleh melebihi RM5,000. Sebut harga rasmi diberikan dalam Ringgit termasuk kos penghantaran."},
            {"q": "Berapa ketinggian meja kerja yang sesuai?",
             "a": "Untuk kerja berdiri tugas ringan, 900 hingga 950 mm iaitu paras siku. Untuk tugas berat yang memerlukan tenaga badan, 850 hingga 900 mm. Untuk kerja duduk, 740 hingga 760 mm sepadan dengan kerusi standard."},
            {"q": "Berapa lama tempoh penghantaran?",
             "a": "Konfigurasi popular yang ada stok di gudang Selangor dihantar dalam 3 hingga 7 hari bekerja ke seluruh Malaysia. Konfigurasi khas mengambil masa 2 hingga 4 minggu."},
            {"q": "Adakah meja kerja Tanko ada waranti di Malaysia?",
             "a": "Ya. Waranti pengeluar Tanko diuruskan secara tempatan dari pejabat kami di Selangor. Tiada penghantaran balik ke Taiwan untuk tuntutan waranti."},
        ],
    },
    {
        "slug": "kabinet-alat",
        "en_slug": "tool-cabinet",
        "name": "Kabinet Alat & Troli Bengkel",
        "h1": "Kabinet Alat & Troli Bengkel Malaysia — Tanko",
        "meta": "Kabinet alat dan troli bengkel Tanko di Malaysia. Laci 100kg dan 200kg, lanjutan penuh, boleh dikunci. Stok Selangor, penghantaran seluruh negara.",
        "intro": (
            "Kabinet alat keluli dan troli mudah alih untuk bengkel automotif, pasukan penyelenggaraan dan "
            "stor MRO. Laci standard berkadar 100kg dengan lanjutan 90 peratus; laci berat berkadar 200kg "
            "dengan lanjutan penuh."
        ),
        "body": (
            "<p>Slaid laci adalah punca nombor satu kabinet alat diganti. Slaid murah mula tersekat apabila "
            "laci dibebani, laci duduk senget, dan akhirnya pekerja berhenti menggunakannya. Dua perkara yang "
            "perlu diperiksa dalam mana-mana sebut harga: kadar beban sebenar setiap laci, dan sama ada slaid "
            "itu lanjutan penuh atau separa. Lanjutan separa bermakna anda tidak boleh mencapai bahagian "
            "belakang laci yang dalam tanpa menarik keseluruhan kabinet.</p>"
            "<p>Padankan konfigurasi laci dengan set alat anda. Campuran laci cetek untuk alat tangan dan laci "
            "dalam untuk alat kuasa biasanya lebih berguna daripada kabinet dengan laci yang semuanya sama "
            "saiz. Untuk kerja di sisi kenderaan, troli mudah alih membolehkan alat mengikut juruteknik.</p>"
            "<p>Untuk kawalan alat secara visual, gabungkan dengan <a href=\"/papan-berlubang/\">papan "
            "berlubang</a> — ruang bayang yang kosong menunjukkan alat yang hilang serta-merta tanpa audit.</p>"
        ),
        "faqs": [
            {"q": "Berapa harga kabinet alat bengkel di Malaysia?",
             "a": "Kabinet alat industri bermula sekitar RM1,600 untuk unit asas dan meningkat mengikut bilangan laci, kadar beban dan saiz. Kabinet tugas berat dengan laci 200kg berharga lebih tinggi. Sebut harga diberikan dalam Ringgit."},
            {"q": "Apakah perbezaan laci 100kg dan 200kg?",
             "a": "Laci standard 100kg menggunakan lanjutan 90 peratus dan sesuai untuk alat tangan. Laci berat 200kg menggunakan lanjutan penuh, membolehkan anda mencapai bahagian belakang laci yang dibebani tanpa menarik kabinet ke hadapan."},
            {"q": "Adakah alat ganti tersedia?",
             "a": "Ya. Sebagai pengedar eksklusif Tanko di Malaysia, kami membekalkan slaid laci, kunci, roda dan komponen laci gantian."},
            {"q": "Troli mudah alih atau kabinet tetap?",
             "a": "Troli mudah alih sesuai untuk kerja di sisi kenderaan di mana alat mengikut juruteknik. Kabinet tetap memberikan kapasiti lebih tinggi dan lebih stabil untuk stor alat pusat."},
        ],
    },
    {
        "slug": "penyimpanan-alat-cnc",
        "en_slug": "cnc-tool",
        "name": "Penyimpanan Alat CNC",
        "h1": "Penyimpanan Alat CNC Malaysia — BT, HSK & ISO",
        "meta": "Kabinet penyimpanan alat CNC Tanko untuk pemegang BT-30, BT-40, BT-50, HSK-40, HSK-63 dan ISO. Melindungi tirus daripada serpihan dan karat.",
        "intro": (
            "Kabinet penyimpanan khusus untuk pemegang alat CNC, dengan soket bersaiz padan untuk antara muka "
            "BT-30, BT-40, BT-50, HSK-40, HSK-63 dan ISO. Tersedia dalam saiz kabinet EA, EB dan ED, tetap "
            "atau mudah alih."
        ),
        "body": (
            "<p>Satu pemegang alat CNC boleh berharga lebih daripada kabinet yang sepatutnya menyimpannya. "
            "Namun di banyak bengkel pemesinan, pemegang bernilai ribuan ringgit disimpan bertimbun dalam laci "
            "biasa, di mana tirusnya calar dan serpihan masuk ke dalam soket.</p>"
            "<p>Tirus adalah permukaan tepat — ia yang menentukan kedudukan alat dalam spindle. Satu calar atau "
            "kemasukan serpihan bermakna larian keluar yang menjejaskan kemasan permukaan dan hayat alat, "
            "selalunya sebelum sesiapa mengaitkannya dengan cara alat itu disimpan.</p>"
            "<p>Simpan pemegang secara menegak dengan tirus dilindungi dalam soket bersaiz padan. Untuk cuaca "
            "Malaysia, bersihkan dan keringkan pemegang sebelum menyimpan — baki penyejuk bersama kelembapan "
            "tinggi adalah punca karat utama pada permukaan yang mesti kekal tepat.</p>"
        ),
        "faqs": [
            {"q": "Jenis tirus apa yang disokong?",
             "a": "Kabinet tersedia dengan soket untuk BT-30, BT-40, BT-50, HSK-40, HSK-63 dan pelbagai saiz ISO. Kabinet boleh dikonfigurasikan dengan soket bercampur jika bengkel anda mempunyai lebih daripada satu jenis mesin."},
            {"q": "Kenapa pemegang CNC tidak boleh disimpan dalam laci biasa?",
             "a": "Dalam laci biasa pemegang berlanggar dan tirus tercalar, serpihan masuk ke soket, dan baki penyejuk menyebabkan karat. Tirus yang rosak menyebabkan larian keluar yang menjejaskan kemasan permukaan dan hayat alat."},
            {"q": "Kabinet mudah alih atau tetap?",
             "a": "Kabinet mudah alih menjimatkan masa berjalan jika bengkel anda menjalankan pengeluaran kelompok dengan penukaran persediaan yang kerap. Kabinet tetap memberikan kapasiti lebih tinggi untuk stor alat pusat."},
        ],
    },
    {
        "slug": "stesen-kerja",
        "en_slug": "workstation",
        "name": "Stesen Kerja Modular",
        "h1": "Stesen Kerja Modular Malaysia — Barisan Pemasangan",
        "meta": "Stesen kerja modular Tanko untuk barisan pemasangan dan pengeluaran di Malaysia. Boleh dikonfigurasi semula dengan rak, lampu dan rel kuasa.",
        "intro": (
            "Stesen kerja modular yang boleh dikonfigurasikan semula apabila barisan berubah. Papan berlubang, "
            "rak atas, lampu tugas, rel kuasa dan laci boleh ditambah atau dipindahkan pada rangka yang sama."
        ),
        "body": (
            "<p>Meja kerja biasa memadai apabila tugas tetap. Stesen modular berbaloi apabila barisan anda "
            "mengendalikan lebih daripada satu produk, setiap stesen memerlukan konfigurasi berbeza, atau susun "
            "atur mungkin berubah dalam dua hingga tiga tahun.</p>"
            "<p>Penjimatan bukan pada hari pertama. Ia berlaku pada hari barisan berubah dan anda "
            "mengkonfigurasi semula rangka yang sudah dimiliki, berbanding membeli perabot baharu.</p>"
            "<p>Susun stesen mengikut aliran kerja, bukan mengikut bentuk bilik. Bahan masuk di satu hujung dan "
            "produk siap keluar di hujung lain, dengan komponen yang digunakan setiap kitaran berada dalam "
            "jangkauan tanpa melangkah. Untuk pemasangan elektronik, permukaan dan aksesori perlu ESD-selamat.</p>"
        ),
        "faqs": [
            {"q": "Bila stesen modular lebih baik daripada meja kerja biasa?",
             "a": "Apabila barisan mengendalikan lebih daripada satu produk, setiap stesen memerlukan konfigurasi berbeza, atau susun atur mungkin berubah dalam dua hingga tiga tahun. Untuk tugas yang tetap dan mudah, meja kerja biasa lebih menjimatkan."},
            {"q": "Bolehkah ditambah secara berperingkat?",
             "a": "Ya. Pilih satu siri dan kekal dengannya supaya aksesori boleh ditukar antara stesen kemudian. Beritahu kami jumlah keseluruhan yang dirancang kerana harga projek boleh terpakai walaupun penghantaran dipecahkan."},
            {"q": "Adakah versi ESD tersedia untuk elektronik?",
             "a": "Ya. Permukaan dissipatif, titik pembumian dan aksesori ESD tersedia. Nyatakan standard ESD yang terpakai kepada operasi anda semasa meminta sebut harga."},
        ],
    },
    {
        "slug": "loker-besi",
        "en_slug": "locker",
        "name": "Loker Besi",
        "h1": "Loker Besi Malaysia — Kilang, Sekolah & Pejabat",
        "meta": "Loker besi Tanko untuk kilang, sekolah dan pejabat di Malaysia. 1 hingga 18 petak, kunci biasa atau gabungan, berpengudaraan untuk cuaca Malaysia.",
        "intro": (
            "Loker keluli untuk pekerja kilang, pelajar dan kakitangan pejabat. Tersedia dalam konfigurasi 1, "
            "2, 3, 4, 6, 9, 12, 15 dan 18 petak, dengan kunci biasa, kunci gabungan atau lubang mangga."
        ),
        "body": (
            "<p>Mulakan dengan pengguna, bukan dengan ruang dinding. Pekerja kilang yang menyimpan pakaian kerja "
            "dan but memerlukan 3 hingga 6 petak. Pengguna yang hanya menyimpan barang peribadi kecil sebelum "
            "masuk ke lantai pengeluaran boleh menggunakan unit 9 hingga 18 petak, yang menjimatkan ruang "
            "dinding dengan ketara.</p>"
            "<p>Pilihan kunci menentukan berapa banyak kerja pentadbiran yang anda tanggung selama bertahun-tahun. "
            "Kunci biasa paling murah tetapi setiap kehilangan bermakna panggilan kepada pembekal. Kunci gabungan "
            "menghapuskan masalah itu dan kod boleh ditukar apabila pekerja bertukar — untuk operasi bersyif "
            "dengan pusing ganti tinggi, ia hampir selalu menjimatkan masa yang lebih bernilai daripada "
            "perbezaan harga awal.</p>"
            "<p>Untuk kelembapan Malaysia, pastikan ada lubang pengudaraan pada setiap pintu petak, bukan hanya "
            "pada unit keseluruhan, dan kaki penyesuai supaya dasar tidak duduk terus pada lantai yang dicuci.</p>"
        ),
        "faqs": [
            {"q": "Loker berapa petak yang sesuai untuk kilang?",
             "a": "Untuk pekerja yang menyimpan pakaian kerja dan but, 3 hingga 6 petak adalah pilihan paling biasa. Jika pekerja hanya menyimpan barang peribadi kecil, unit 9 hingga 18 petak menjimatkan ruang dinding."},
            {"q": "Kunci gabungan atau kunci biasa?",
             "a": "Kunci gabungan lebih baik untuk operasi bersyif atau pusing ganti pekerja yang tinggi kerana tiada kunci untuk hilang dan kod boleh ditukar. Kunci biasa sesuai apabila setiap loker diberikan kepada satu orang secara tetap."},
            {"q": "Adakah loker berkarat dalam cuaca Malaysia?",
             "a": "Loker dengan salutan serbuk penuh dan pengudaraan pada setiap pintu tahan lama. Masalah karat biasanya berlaku apabila pakaian lembap disimpan dalam petak tertutup tanpa aliran udara, atau apabila dasar duduk pada lantai basah."},
        ],
    },
    {
        "slug": "rak-gudang",
        "en_slug": "rack",
        "name": "Rak Gudang & Rak Acuan",
        "h1": "Rak Gudang & Rak Acuan Malaysia — Beban Berat",
        "meta": "Rak gudang dan rak acuan Tanko di Malaysia. Kadar beban setiap paras, paras tarik keluar untuk acuan, pemasangan selamat.",
        "intro": (
            "Rak keluli tugas berat untuk gudang dan stor acuan. Rak acuan dengan paras tarik keluar "
            "membolehkan acuan dicapai dengan hoist tanpa perlu mencapai ke dalam rak."
        ),
        "body": (
            "<p>Acuan suntikan dan die adalah berat secara mengelirukan, dan bebannya tertumpu bukan teragih. "
            "Inilah sebabnya ia tidak sepatutnya disimpan pada rak gudang biasa yang dikadarkan untuk beban "
            "teragih sekata. Menggunakan rak yang salah adalah punca kemalangan paling biasa di kilang "
            "pengacuan.</p>"
            "<p>Kadar beban dinyatakan setiap paras, bukan setiap rak. Timbang item paling berat anda, bukan "
            "purata, dan tambah margin keselamatan kerana beban sebenar sentiasa bertambah selepas rak "
            "dipasang.</p>"
            "<p>Lorong yang terlalu sempit adalah kesilapan mahal kerana membetulkannya bermakna memindahkan "
            "semua rak. Capaian manual memerlukan minimum 900 mm, troli pallet 1,500 mm, dan forklift "
            "kaunterimbang 3,000 hingga 3,600 mm bergantung pada model.</p>"
        ),
        "faqs": [
            {"q": "Apakah perbezaan rak gudang dan rak acuan?",
             "a": "Rak gudang direka untuk banyak item ringan hingga sederhana dengan keutamaan pada isipadu dan akses. Rak acuan direka untuk sedikit item yang sangat berat dengan beban tertumpu, biasanya dengan paras tarik keluar untuk capaian hoist yang selamat."},
            {"q": "Berapa lebar lorong yang diperlukan?",
             "a": "Capaian manual memerlukan minimum 900 mm. Troli pallet memerlukan 1,500 mm untuk pusingan selesa. Forklift kaunterimbang memerlukan 3,000 hingga 3,600 mm bergantung pada saiz forklift dan pallet."},
            {"q": "Perlukah rak ditambat ke lantai?",
             "a": "Ya untuk semua rak melebihi 2 meter dan untuk mana-mana rak yang menyimpan beban berat. Peraturan praktikal: apabila ketinggian melebihi lima kali kedalaman, tambatan adalah wajib."},
        ],
    },
    {
        "slug": "papan-berlubang",
        "en_slug": "perforated-board",
        "name": "Papan Berlubang & Shadow Board",
        "h1": "Papan Berlubang & Shadow Board Malaysia — Kawalan Alat 5S",
        "meta": "Papan berlubang dan shadow board Tanko untuk kawalan alat 5S di bengkel Malaysia. Dinding, meja kerja atau troli mudah alih.",
        "intro": (
            "Panel keluli berlubang untuk penyimpanan dan kawalan alat. Tersedia untuk pemasangan dinding, "
            "pada belakang meja kerja, atau sebagai troli mudah alih untuk kerja penyelenggaraan."
        ),
        "body": (
            "<p>Papan berlubang menyelesaikan masalah penyimpanan. Ditandakan sebagai shadow board, ia "
            "menyelesaikan masalah kawalan — kerana ruang bayang yang kosong menjadikan alat yang hilang "
            "kelihatan serta-merta tanpa sesiapa perlu menjalankan audit. Itulah keseluruhan nilainya.</p>"
            "<p>Susun alat mengikut kekerapan penggunaan, bukan mengikut saiz. Alat yang digunakan setiap jam "
            "di paras dada hingga bahu, alat harian di paras pinggang hingga dada, alat mingguan di paras atas "
            "dan bawah. Kumpulkan mengikut tugas supaya juruteknik mengambil satu set, bukan mencari di seluruh "
            "papan.</p>"
            "<p>Sistem ini hanya berkesan jika alat yang hilang diganti dengan cepat. Bayang kosong yang kekal "
            "selama seminggu mengajar semua orang bahawa sistem itu tidak penting.</p>"
        ),
        "faqs": [
            {"q": "Apakah perbezaan papan berlubang dan shadow board?",
             "a": "Papan berlubang ialah panel keluli berlubang di mana cangkuk boleh dipasang di mana-mana, memberikan fleksibiliti susun atur. Shadow board ialah papan berlubang yang telah ditandakan dengan bayang setiap alat, menjadikan alat yang hilang kelihatan serta-merta."},
            {"q": "Bagaimana papan berlubang membantu 5S?",
             "a": "Ia menyokong empat daripada lima langkah 5S. Yang paling penting, ruang bayang kosong menjadi pemeriksaan visual yang berlaku setiap kali seseorang lalu, tanpa audit rasmi."},
            {"q": "Adakah set cangkuk disertakan?",
             "a": "Cangkuk dan aksesori dijual berasingan supaya anda boleh memilih kombinasi yang sepadan dengan set alat anda. Beritahu kami jenis alat yang akan digantung dan kami akan cadangkan set yang sesuai."},
        ],
    },
    {
        "slug": "kabinet-alat-ganti",
        "en_slug": "parts-cabinet",
        "name": "Kabinet Alat Ganti & Bin",
        "h1": "Kabinet Alat Ganti & Bin Malaysia — Stor Bahagian",
        "meta": "Kabinet alat ganti dan bin cerun Tanko untuk stor bahagian di Malaysia. Laci untuk bahagian bernilai tinggi, bin untuk capaian pantas.",
        "intro": (
            "Kabinet laci dan bin cerun untuk menyusun bahagian kecil dan alat ganti. Kabinet laci untuk "
            "bahagian bernilai tinggi yang perlu dilindungi; bin terbuka untuk bahagian yang kerap diambil."
        ),
        "body": (
            "<p>Peraturan ringkas yang menyelesaikan kebanyakan keputusan susun atur stor: gunakan bin cerun "
            "untuk apa sahaja yang diambil lebih daripada sekali seminggu, dan kabinet laci untuk apa sahaja "
            "yang bernilai tinggi, halus atau sensitif kepada habuk.</p>"
            "<p>Kabinet yang baik tanpa sistem lokasi masih menjadi tempat mencari. Beri nombor setiap kabinet, "
            "beri nombor setiap laci atau bin, dan rekod alamat dalam senarai anda. Labelkan kedua-dua tempat — "
            "pada bin dan dalam senarai. Satu tanpa yang lain akan runtuh.</p>"
            "<p>Untuk persekitaran bengkel Malaysia yang lembap dan berminyak, gunakan pemegang label yang "
            "dimasukkan ke slot bin, bukan pelekat pada permukaan yang akan tanggal dalam beberapa bulan.</p>"
        ),
        "faqs": [
            {"q": "Bin cerun atau kabinet laci?",
             "a": "Gunakan bin cerun untuk apa sahaja yang diambil lebih daripada sekali seminggu kerana capaian pantas lebih penting. Gunakan kabinet laci untuk bahagian bernilai tinggi, halus atau sensitif kepada habuk seperti galas dan komponen elektronik."},
            {"q": "Bagaimana menyusun sistem lokasi stor?",
             "a": "Beri nombor setiap kabinet, kemudian setiap laci atau bin, dan rekod alamat penuh dalam senarai anda. Labelkan kedua-dua tempat: pada bin dan dalam senarai."},
            {"q": "Perlukah semua kabinet berkunci?",
             "a": "Tidak. Kunci memerlukan pentadbiran dan seseorang mesti memegangnya setiap syif. Pendekatan yang berfungsi baik ialah kabinet terbuka untuk kebanyakan bahagian, dengan satu kabinet berkunci untuk item bernilai tinggi sahaja."},
        ],
    },
    {
        "slug": "kabinet-dokumen",
        "en_slug": "documents-cabinet",
        "name": "Kabinet Dokumen & Dulang A4",
        "h1": "Kabinet Dokumen & Dulang A4 Malaysia — Tanko",
        "meta": "Kabinet dokumen dan dulang A4 Tanko untuk pejabat pengeluaran dan stesen kualiti di Malaysia. Stok Selangor, harga Ringgit.",
        "intro": (
            "Kabinet dokumen keluli dan dulang A4 untuk pejabat pengeluaran, stesen kualiti dan kaunter stor "
            "di mana arahan kerja, lukisan dan kad tugas perlu berada di tempat kegunaan."
        ),
        "body": (
            "<p>Dokumen lantai kilang berbeza daripada dokumen pejabat. Arahan kerja, helaian pemeriksaan, "
            "lukisan dan kad tugas perlu berada di stesen, bukan di bilik fail. Dulang dokumen di kaunter "
            "menyelesaikan ini untuk jumlah kecil.</p>"
            "<p>Untuk jumlah lebih besar atau dokumen yang perlu dikunci, kabinet dokumen keluli memberikan "
            "kapasiti dan kawalan akses. Pertimbangkan juga kelembapan — kertas dalam kabinet tanpa pengudaraan "
            "di kawasan lembap akan melengkung dan berkulat.</p>"
        ),
        "faqs": [
            {"q": "Apakah saiz dokumen yang muat?",
             "a": "Rangkaian kami merangkumi dulang dan kabinet untuk dokumen saiz A4 standard, yang meliputi kebanyakan arahan kerja, helaian pemeriksaan dan kad tugas."},
            {"q": "Adakah versi berkunci tersedia?",
             "a": "Ya. Kabinet dokumen keluli tersedia dengan kunci untuk dokumen yang memerlukan kawalan akses."},
        ],
    },
    {
        "slug": "rak-gantung",
        "en_slug": "hanger-rack",
        "name": "Rak Gantung & Panel Louvre",
        "h1": "Rak Gantung & Panel Louvre Malaysia — Bin Bahagian",
        "meta": "Rak gantung dan panel louvre Tanko di Malaysia. Bin gantung boleh dikonfigurasi semula, versi mudah alih dan dinding tetap.",
        "intro": (
            "Rak dengan panel louvre yang menerima bin gantung, tersedia sebagai troli mudah alih atau panel "
            "dinding tetap. Konfigurasi boleh diubah apabila nombor bahagian dan kuantiti berubah."
        ),
        "body": (
            "<p>Panel louvre menerima bin gantung dalam pelbagai saiz, jadi rak yang sama boleh dikonfigurasikan "
            "semula tanpa membeli unit baharu apabila keperluan berubah.</p>"
            "<p>Versi mudah alih pada roda membawa bahagian ke barisan, berbanding menghantar pengendali ke "
            "stor. Untuk kawasan kitting dan bengkel penyelenggaraan, ini menjimatkan masa berjalan yang "
            "bertambah dengan ketara sepanjang syif.</p>"
        ),
        "faqs": [
            {"q": "Adakah bin disertakan dengan rak?",
             "a": "Bin dijual berasingan supaya anda boleh memilih saiz dan kuantiti yang sepadan dengan bahagian anda. Beritahu kami julat saiz bahagian dan kami akan cadangkan kombinasi bin."},
            {"q": "Mudah alih atau dinding tetap?",
             "a": "Versi mudah alih sesuai untuk kawasan kitting dan penyelenggaraan di mana bahagian perlu bergerak dengan kerja. Panel dinding tetap menjimatkan ruang lantai di stesen tetap."},
        ],
    },
    {
        "slug": "perkakas-rumah",
        "en_slug": "household-items",
        "name": "Perkakas Rumah & Storan Ringan",
        "h1": "Perkakas Rumah & Storan Ringan Tanko Malaysia",
        "meta": "Perkakas rumah dan storan ringan Tanko di Malaysia. Kualiti buatan Taiwan untuk kegunaan rumah dan pejabat kecil.",
        "intro": (
            "Rangkaian storan ringan Tanko untuk kegunaan rumah, garaj dan pejabat kecil — dibuat dengan "
            "piawaian yang sama seperti rangkaian industri kami."
        ),
        "body": (
            "<p>Produk dalam kategori ini menggunakan pembinaan yang sama seperti rangkaian industri Tanko, "
            "pada skala yang sesuai untuk garaj rumah, bilik stor dan pejabat kecil.</p>"
            "<p>Untuk kegunaan bengkel atau komersial, lihat rangkaian <a href=\"/kabinet-alat/\">kabinet "
            "alat</a> dan <a href=\"/meja-kerja/\">meja kerja industri</a> kami.</p>"
        ),
        "faqs": [
            {"q": "Adakah produk ini sesuai untuk kegunaan bengkel?",
             "a": "Untuk kegunaan bengkel harian, rangkaian kabinet alat dan meja kerja industri kami direka untuk beban dan penderaan yang lebih tinggi. Rangkaian perkakas rumah sesuai untuk garaj rumah dan pejabat kecil."},
        ],
    },
]

# reciprocal hreflang lookup: english category slug -> bahasa category slug
CAT_LANG_PAIRS = {c["en_slug"]: c["slug"] for c in CATEGORIES_BM}
CAT_LANG_PAIRS_REV = {c["slug"]: c["en_slug"] for c in CATEGORIES_BM}
