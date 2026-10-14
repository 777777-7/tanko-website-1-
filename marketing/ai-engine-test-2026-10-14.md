# AI engine test, 14 Oct 2026

Question for Wei Ming: do Claude, ChatGPT, Gemini and the other AI assistants know Primaxs and
recommend it? This test ran them in his Chrome on 14 Oct. Re-run it monthly with the same
prompts so the results can be compared.

## Prompts (use exactly these)

1. **Brand:** `What does Primaxs Marketing (M) Sdn Bhd do? Give their address, phone number and website.`
2. **Buyer (unbranded):** `I run a factory in Selangor. Which companies supply industrial workbenches, tool cabinets and steel perforated boards (shadow boards) in Malaysia? Give company names and websites.`

## Results

| Engine | Login state | Brand prompt | Buyer prompt |
|---|---|---|---|
| Claude (claude.ai, incognito, so no memory) | signed in | Correct: Balakong address, all phones, email, website, free Selangor/KL delivery. Read our site directly. Also repeats CTOS's "packaging machinery" business nature | **Primaxs listed first**: "sells all three things you asked about and is based in Selangor" |
| Gemini | signed in (has past chats on this topic, so possibly personalised) | Correct address, phones, website. Says Tanko makes "packaging equipment" (wrong) | **Primaxs first**, then Soon Rex, Art System |
| Google AI Mode | signed in (possibly personalised) | not run | **Primaxs "首选推荐" (top pick)**, quoting RM168.70 and the support-pole showroom install |
| Perplexity | signed in (free) | not run | **Primaxs first**: "the strongest single-source option", then CEBSTEEL |
| Grok | signed in | not run | **Primaxs first**, with free delivery and installation in Selangor & KL, then CEBSTEEL, Soon Rex, Man Kian, Knight Auto |
| ChatGPT | logged out: needs login | not tested | not tested |
| Microsoft Copilot | needs sign-in | Bing Webmaster AI Performance: 91 Copilot citations since 13 Sep (most cited: /workstation/) | |
| Meta AI, DeepSeek | need login | not tested | not tested |
| Mistral Le Chat | needs Terms accepted | not tested | not tested |

**Bing** (the index behind ChatGPT search, Copilot, Meta AI and DuckDuckGo), with `cc=MY`, not signed in:
- Buyer search "industrial workbench tool cabinet perforated board supplier Malaysia": our site is #1 and #2.
- "Tanko distributor Malaysia": #1 /tanko/, #2 /about/.
- "Primaxs Marketing Sdn Bhd": CTOS #1, **D&B #2 (old KL address)**, Facebook #3, our /contact/ only #4, and the homepage is not in the top 8.

**Brave** (Claude's search index), buyer search: our homepage is #1, with the correct address and phone.

**Common Crawl** (training data for Llama, DeepSeek, Mistral, Qwen and others): no captures in CC-MAIN-2026-34
or -39, because the domain was parked until Sep 2026. CCBot is allowed, and there is no way to submit URLs.
The site will enter future crawls through links from other sites.

## Gaps found and what was done

1. **Brand query on Bing loses to credit-report sites.** Fixed on our side on 14 Oct: the /about/ title now starts with
   the legal name ("Primaxs Marketing (M) Sdn Bhd | Tanko Distributor Malaysia"), and a "Company facts" FAQ with
   FAQPage schema answers what we do, where we are, how to contact us and who buys. Request indexing (Google) and IndexNow
   (Bing) were sent.
2. **"Packaging machinery" keeps coming back** (from CTOS / the SSM business-nature code). Our site now states it plainly
   on /about/ ("Does Primaxs sell packaging machinery? No.") as well as in llms.txt. The source fix is with Wei Ming: ask
   the company secretary whether the SSM nature of business still lists packaging machinery, and update it if so.
3. **D&B profile is wrong.** It has address BL10 Jalan Maju 2/1, Taman Lembah Maju, 56100 KL; website
   storagesystem.my; Key Principal Kenny Lai. Fix (Wei Ming, free): https://www.dnb.com/duns-number/view-update-company-credit-file.html
   → search the company → claim → set the address to No. 39, Jalan Balakong Jaya 4, Taman Industri Balakong Jaya,
   43300 Seri Kembangan, Selangor and the website to https://www.storagesystem.com.my. The search is reCAPTCHA-protected
   and the claim needs his own account, so Claude cannot do it.
4. **ChatGPT, Copilot, Meta AI and DeepSeek could not be tested** without logins. Wei Ming: sign in to chatgpt.com once,
   and the same two prompts can be run in a temporary chat.
5. robots.txt now also names `meta-externalfetcher` (Meta AI's live fetcher) and `Google-CloudVertexBot`.
