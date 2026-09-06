/* NEWPAGES business-listing re-fill.
 *
 * Fills every field of the Primaxs claim form except the SSM PDF (which has to
 * be picked from disk) and the reCAPTCHA (which always has to be a person).
 *
 * HOW TO USE
 *   1. Log in to NEWPAGES.
 *   2. Open https://m.newpages.com.my/en/93368/business-listing.html
 *      (the www version of this path 404s -- it must be the m. subdomain)
 *   3. Open DevTools (F12) -> Console, paste this whole file, press Enter.
 *   4. Attach the SSM certificate PDF, choose the logo and banner from
 *      marketing/newpages/, tick the reCAPTCHA, Submit.
 *
 * The logo and banner cannot be set by script -- browsers do not allow a file
 * input to be populated from JavaScript. Pick them by hand:
 *      marketing/newpages/logo-800x800.png     -> Company Logo
 *      marketing/newpages/banner-860x360.png   -> Company Banner
 */

(function () {
  var form = [].slice.call(document.querySelectorAll('form'))
    .filter(function (f) { return /Registered No/i.test(f.innerText); })[0];

  if (!form) {
    console.error('NEWPAGES: business-listing form not found. Are you logged in, on the m. subdomain, and on the right page?');
    return;
  }

  function set(selector, value) {
    var el = form.querySelector(selector);
    if (!el) { console.warn('missing: ' + selector); return false; }
    var proto = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype
              : el.tagName === 'SELECT'   ? HTMLSelectElement.prototype
              : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, value);
    ['input', 'change', 'keyup'].forEach(function (ev) {
      el.dispatchEvent(new Event(ev, { bubbles: true }));
    });
    return true;
  }

  var BUSINESS_TYPE =
    'Industrial Storage Equipment Distributor - Workbenches, Tool Cabinets, ' +
    'CNC Tool Storage, Steel Lockers, Warehouse Racking, Workstations, ' +
    'Perforated Boards';

  var PRODUCTS =
    'Primaxs Marketing (M) Sdn Bhd is the exclusive Malaysia distributor for ' +
    'Tanko Enterprise Co., Ltd. (Taiwan, established 1975). We supply ' +
    'approximately 1,700 SKUs across 11 ranges: industrial workbenches in ' +
    'medium and heavy duty specifications; tool cabinets and roller trolleys; ' +
    'CNC tool storage fitted for BT-30, BT-40, BT-50, HSK-40, HSK-63 and ISO ' +
    'holders; modular workstations; steel lockers; parts and document ' +
    'cabinets; warehouse racking; mould racks; and perforated boards with ' +
    'hooks and hangers.\n\n' +
    'Stock is held in Selangor for popular configurations, with 3 to 7 working ' +
    'day delivery in the Klang Valley and nationwide delivery across ' +
    'Peninsular Malaysia, Sabah and Sarawak. All quotations are issued in ' +
    'Malaysian Ringgit with unit pricing, project pricing and delivery costs ' +
    'itemised separately. Delivery and installation are free within Selangor ' +
    'and the Klang Valley; outstation delivery is quoted separately. The ' +
    'manufacturer warranty against manufacturing defects runs 1 year and is ' +
    'administered locally from our Selangor office.\n\n' +
    'We supply manufacturing plants, automotive workshops, CNC machining ' +
    'shops, laboratories and cleanrooms, electronics and EMS facilities, food ' +
    'and pharmaceutical production, warehouses, schools, campuses and ' +
    'technical training centres across Malaysia.';

  set('input[name=company_name]',          'Primaxs Marketing (M) Sdn Bhd');
  set('input[name=company_registered_no]', '200601036829 (756588-H)');
  set('input[name=company_address]',       'No. 39, Jalan Balakong Jaya 4, Taman Industri Balakong Jaya, 43300 Seri Kembangan, Selangor');
  set('select[name=location]',             '21');            // 21 = Selangor
  set('input[name=latitude]',              '3.01217');
  set('input[name=longitude]',             '101.75234');
  set('input[name=email]',                 'sales@storagesystem.my');
  set('input[name=tel]',                   '+60 3-4296 4737');
  set('input[name=phonenumber]',           '+60 12-616 3088');
  set('input[name=website]',               'https://www.storagesystem.com.my');
  set('input[name=fb_page_url]',           'https://www.facebook.com/primaxsmarketing');
  set('textarea[name=business_type]',      BUSINESS_TYPE);
  set('textarea[name=describe_your_product_service]', PRODUCTS);

  // Business Classified -- the free tier caps at 4, a 5th tick is refused.
  //   1827 Storage System (16 listings)  -- exact fit, easiest #1 on the platform
  //   608  Hardware (357)                -- biggest hardware category
  //   1860 Industrial Equipment (175)    -- main industrial category
  //   1226 Material Handling Equipment (57) -- warehouse & racking buyers
  var WANT = ['1827', '608', '1860', '1226'];
  var boxes = [].slice.call(form.querySelectorAll('input[name="business_classified[]"]'));

  boxes.filter(function (b) { return b.checked && WANT.indexOf(b.value) === -1; })
       .forEach(function (b) { b.click(); });          // clear anything unwanted first

  WANT.forEach(function (v) {
    var b = boxes.filter(function (x) { return x.value === v; })[0];
    if (b && !b.checked) { b.click(); }
  });

  var checked = boxes.filter(function (b) { return b.checked; }).length;

  console.log('NEWPAGES form filled. Categories ticked: ' + checked + '/4');
  console.log('Still to do by hand:');
  console.log('  1. Company Logo    -> marketing/newpages/logo-800x800.png');
  console.log('  2. Company Banner  -> marketing/newpages/banner-860x360.png');
  console.log('  3. SSM Document    -> the registration certificate PDF (required)');
  console.log('  4. reCAPTCHA, then Submit');
})();
