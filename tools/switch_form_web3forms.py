# Switch the enquiry form from formsubmit.co (down since 29 Oct 2026) to Web3Forms.
import io
KEY = '3b1f65ac-8ded-47b0-8758-bc0cafa7ef83'
OLD_HEAD = '''            action="https://formsubmit.co/weimingwong78@gmail.com"
            method="POST" novalidate>
        <input type="hidden" name="_subject" value="Primaxs — new quote request">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">'''
NEW_HEAD = f'''            action="https://api.web3forms.com/submit"
            method="POST" novalidate>
        <input type="hidden" name="access_key" value="{KEY}">
        <input type="hidden" name="subject" value="Primaxs — new quote request">
        <input type="hidden" name="from_name" value="storagesystem.com.my">
        <input type="checkbox" name="botcheck" class="hidden" style="display:none" tabindex="-1" autocomplete="off">'''
def sub(p, pairs):
    s = io.open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) >= 1, (p, a[:60])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', p)
for p in ['docs/enquiry/index.html', 'site/templates/enquiry.html']:
    sub(p, [(OLD_HEAD, NEW_HEAD)])
for p in ['docs/assets/js/enquiry.js', 'site/static/js/enquiry.js']:
    sub(p, [('var ajaxUrl = "https://formsubmit.co/ajax/weimingwong78@gmail.com";',
             'var ajaxUrl = "https://api.web3forms.com/submit";')])
sub('docs/privacy/index.html', [
    ('enquiry form details via FormSubmit', 'enquiry form details via Web3Forms'),
    ('<strong>FormSubmit</strong> (formsubmit.co)', '<strong>Web3Forms</strong> (web3forms.com)'),
    ('<li><strong>FormSubmit</strong> &mdash;', '<li><strong>Web3Forms</strong> &mdash;'),
])
