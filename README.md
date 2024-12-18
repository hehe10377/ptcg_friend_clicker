# PTCG 神包好友連點器 (PTCG Friend Clicker for God Packs)

**搶神包加不到好友很痛苦嗎？**😩  
在 PTCG 中，因為好友上限問題，無法成功發送好友請求的情況很常見，尤其是在搶神包的高峰期。  

別擔心，**PTCG 神包好友連點器**讓你快速、高效地自動點擊好友請求，幫助你成功進入對方的好友清單，抓住搶神包的機會！  

---

## 功能特色  

- **高效連點**：自動快速發送好友請求，直到成功加入清單或達到設定上限。  
- **自動重試**：添加失敗時，工具會自動再次嘗試。  
- **通知功能**：成功加入好友清單後自動發送 Email 通知。  
<!-- - **自訂點擊速度**：自由調整點擊間隔時間，提升成功率。   -->
---

## 安裝指南  

1. **下載專案**：  
   ```bash
   git clone https://github.com/Ying-Kai-Liao/ptcg_friend_clicker
   ```  

2. **進入目錄**：  
   ```bash
   cd ptcg-friend-clicker
   ```  

3. **安裝依賴項**：  
   ```bash
   pip install -r requirements.txt
   ```  

4. **設定環境變數**：  
   在專案目錄中新增一個 `.env` 檔案，並填入以下內容：  
   ```env
   SENDER_EMAIL=your_email@gmail.com
   RECEIVER_EMAIL=recipient_email@gmail.com
   EMAIL_PASSWORD=your_gmail_app_password
   ```  

---

## 如何取得 Gmail App Password  

### 步驟  

1. **登入你的 Gmail 帳號**：  
   前往 [Google 帳號](https://myaccount.google.com/) 頁面，點擊左側的「安全性」。  

2. **啟用雙步驗證(2FA)**：  
   - 在「登入 Google」區塊，確認雙步驗證已啟用。  
   - 如果尚未啟用，請依照指示設定雙步驗證。  

3. **生成 App Password**：  
   - 回到「安全性」頁面，在「登入 Google」區塊找到「應用程式密碼」。  
   - 點擊「應用程式密碼」，輸入你的 Google 密碼進行驗認。  
   - 前往 [App Passwords 設定](https://myaccount.google.com/apppasswords)，選擇應用程式（例如「郵件」）和裝置（例如「Windows 電腦」），然後點擊「生成」。  
   - 你將獲得一組 16 位數的 App Password，請姊守保存，並將其填入 `.env` 檔案的 `EMAIL_PASSWORD` 中。  
> 注意：寄件者信箱 (`SENDER_EMAIL`) 和收件者信箱 (`RECEIVER_EMAIL`) 可以設定為同一個 Gmail 帳號。這樣你就能用同一個信箱發送和接收通知。


---

## 使用方法  

1. 啟動程式：  
   ```bash
   python auto_add_friend.py
   ```  
   啟動後，系統會導向你完成以下設置：  
   - 中文或是英文(預設中文)
   - 要不要設定按鈕位置(通常是要)
   - 要不要發送email通知(需要另外設定env)

2. 工具會自動開始連點好友請求按鈕。  

3. 當成功送出好友邀請時，工具會通知你，並結束連點。  

4. 結束程式：
   - 按住 `Delete` 鍵可以正常結束程式(按到停下為止喔!)
   - 按下 `Ctrl+C` 也可以強制結束程式
   
   程式結束時會顯示結束訊息。


---

## 使用場景示範  

下面是一個搶神包時的實際操作影片：  

[**點擊觀看示範影片**](https://youtu.be/To456YkSjUo)  
(影片使用[**雷電模擬器**](https://www.ldplayer.tw/blog/24307.html))

---

## 注意事項  

- **工具適用於 PTCG 的搶好友請求場景**，特別是因好友上限問題無法成功添加的情況。  
- 請確保你搶神包的 ID 是正確的。
- 本工具僅供學術研究及個人使用，請勿進行任何違反遊戲規章的操作。  

---  

讓這款工具幫助你，從此不再錯過神包的機會！🎉

