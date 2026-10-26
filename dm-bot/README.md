# dateunoa dm-bot: automatic comment-to-DM for the story reels

When someone comments a story reel's keyword (TEXT, REPLY, ASK...), this bot sends them that reel's ending by private DM within seconds and leaves a short public reply ("Sent! Check your DMs 🤍").

- The DMs come from `content/stories/dm_index.json` in this repo. Every new episode updates that file automatically (the story-reel run executes `tools/build_dm_index.py` and pushes), so **there is nothing to update per video.**
- Keywords are unique per episode, so each comment gets the ending of the video it was posted on.
- Instagram allows one private reply per comment, within 7 days of the comment. The bot never sends twice to the same comment.

## One-time setup (about 30-45 minutes, then Meta's review)

### 1. Put the bot online (Replit)
1. In Replit: **Create Repl → Import from GitHub →** `majddarawshe96-lang/dateunoa-reels`.
2. Set the Run command to: `pip install -r dm-bot/requirements.txt && python dm-bot/app.py`
3. Add **Secrets**: `VERIFY_TOKEN` (any random phrase you invent) and `ADMIN_KEY` (another random phrase). Leave the others for step 2.
4. **Deploy → Reserved VM** (the smallest size is enough). Reserved VM keeps the bot awake and keeps its small state file (token refresh, sent comments). Copy the deployment URL, e.g. `https://dateunoa-dm-bot.replit.app`.
5. Open the URL. It should say `dateunoa dm-bot running`.

### 2. Create the Meta app (developers.facebook.com)
1. **My Apps → Create app →** use case **"Manage messaging & content on Instagram"**. It must be a Business type app. Connect it to your business portfolio.
2. In **Instagram → API setup with Instagram login**:
   - **Add account** → log in as **@dateunoa**. It must be a Professional account; it already is.
   - **Generate token** → copy it into the Replit secret `IG_ACCESS_TOKEN`. Copy the Instagram account id shown next to it into `IG_USER_ID`.
3. **App settings → Basic →** copy **App secret** into the Replit secret `APP_SECRET`. Restart the deployment.
4. Back in **API setup → Configure webhooks**:
   - Callback URL: `https://<your-replit-url>/webhook`
   - Verify token: the same `VERIFY_TOKEN`
   - Click **Verify and save**, then **subscribe to the `comments` field**.
5. On the phone, in the Instagram app: **Settings → Messages and story replies → Message controls → Connected tools → Allow access to messages: ON**.

### 3. Test it (works before Meta's review)
1. In the Meta app go to **App roles → Roles → Add people → Instagram testers** and add a second Instagram account you own. Accept the invite in that account (Instagram app → Settings → Website permissions → Apps and websites).
2. From that tester account, comment `TEXT` on any @dateunoa post.
3. Within a few seconds the tester account should get the DM and see the public reply.
4. `https://<your-replit-url>/status?key=<ADMIN_KEY>` shows the live keywords and how many DMs were sent.
   To try without sending anything, add the secret `DRY_RUN=1`; the bot will only log what it would send.

### 4. Go live for everyone: Meta App Review
Until the review passes, only app testers get DMs. To answer real followers:
1. **App settings → Basic:** add the privacy policy URL `https://github.com/majddarawshe96-lang/dateunoa-reels/blob/main/dm-bot/PRIVACY.md`, a category (Lifestyle), and an app icon.
2. Complete **Business verification** for your business portfolio if Meta asks (Business settings → Security center).
3. **App Review → Permissions and features:** request Advanced Access for
   `instagram_business_basic`, `instagram_business_manage_comments`, `instagram_business_manage_messages`.
   For each one, describe the use ("When a user comments a keyword on our reel, we send them one private reply with the story ending they asked for, and a public reply confirming it was sent") and upload a short screen recording of the step 3 test.
4. After approval, switch the app from **Development** to **Live**.
Review usually takes a few days to a couple of weeks. Until then, run the reels with ManyChat or answer DMs manually.

## Facebook page (optional, later)
The bot also answers keyword comments on the Facebook page if you set `FB_PAGE_ID` and `FB_PAGE_TOKEN` (a page access token with `pages_messaging`, `pages_read_engagement`, `pages_manage_metadata`). Then subscribe the page to the **feed** webhook field. This needs the same App Review for those permissions.

## How it decides what to send
- It reacts to top-level comments only. Replies are ignored, including its own public replies.
- The keyword must be a separate word, in any case: "TEXT", "text pls", "Text!" all match; "context" doesn't.
- Your own comments are ignored.
- If GitHub can't be reached, it keeps using the last copy of the DM list it loaded.

Run the tests with `cd dm-bot && python -m pytest -q`.
