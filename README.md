# PTCG 神包好友連點器 (PTCG Friend Clicker for God Packs)

**搶神包加不到好友很痛苦嗎？**😩  
在 PTCG 中，因為好友上限問題，無法成功發送好友請求的情況很常見，尤其是在搶神包的高峰期。  

別擔心，**PTCG 神包好友連點器**讓你快速、高效地自動點擊好友請求，幫助你成功進入對方的好友清單，抓住搶神包的機會！  

---

## 功能特色  

- **高效連點**：自動快速發送好友請求，直到成功加入清單或達到設定上限。  
- **自動重試**：遇到使服器繁忙或添加失敗時，工具會自動再次嘗試。  
- **自訂點擊速度**：自由調整點擊間隔時間，提升成功率。  
- **通知功能**：成功加入好友清單後自動發送 Email 通知。  

---

## 安裝指南  

1. **下載專案**：  
   ```bash
   git clone https://github.com/yourusername/ptcg-friend-clicker.git
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

2. **啟用雙步驗證**：  
   - 在「登入 Google」區塊，確認雙步驗證已啟用。  
   - 如果尚未啟用，請依照指示設定雙步驗證。  

3. **生成 App Password**：  
   - 回到「安全性」頁面，在「登入 Google」區塊找到「應用程式密碼」。  
   - 點擊「應用程式密碼」，輸入你的 Google 密碼進行驗認。  
   - 前往 [App Passwords 設定](https://myaccount.google.com/apppasswords)，選擇應用程式（例如「郵件」）和裝置（例如「Windows 電腦」），然後點擊「生成」。  
   - 你將獲得一組 16 位數的 App Password，請姊守保存，並將其填入 `.env` 檔案的 `EMAIL_PASSWORD` 中。  

---

## 使用方法  

1. 啟動程式：  
   ```bash
   python main.py
   ```  
   啟動後，系統會導向你完成以下設置：  
   - 輸入神包主的好友代碼或 ID。  
   - 設定連點次數上限，或讓工具持續連點直到手動停止。  

2. 工具會自動開始連點好友請求按鈕，並顯示當前嘗試次數。  

3. 當成功加入清單時，工具會通知你，並結束連點。  

---

## 使用場景示範  

下面是一個搶神包時的實際操作影片，讓你看看工具有多高效：  

[**點擊觀看示範影片**](#)  
（此處可插入示範影片連結或嵌入影片）  

---

## 注意事項  

- **工具適用於 PTCG 的搶好友請求場景**，特別是因好友上限問題無法成功添加的情況。  
- 請確保你搶神包的 ID 是正確的，以免浪費連點資源。  
- 本工具僅供學術研究及個人使用，請勿進行任何違反遊戲規章的操作。  

---

## 貢獻  

如果你對此工具有更好的想法或建議，歡迎提交 Issue 或 Pull Request，我們一起讓搶神包變得更高效！  

---  

讓這款工具幫助你，從此不再錯過神包的機會！🎉

