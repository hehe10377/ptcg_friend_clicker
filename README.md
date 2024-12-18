# PTCG 神包好友連點器 (PTCG Friend Clicker for God Packs)

**搶神包加不到好友很痛苦嗎？** 😩  
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

## 初始設定

一般情況下，預設的亮度設定已經足夠使用。如果遇到辨識問題，你可以依照以下步驟重新調整按鈕位置和亮度校準。(如無法自動停止)

1. **執行設定程式**：
   ```bash
   python adjust_brightness.py
   ```

2. **跟隨三步驟設定**：
   - **步驟一**：準備設定
     - 找一個可以成功發送好友請求的玩家
     - 打開與該玩家的主頁(交友邀請那裡)
   
   - **步驟二**：設定按鈕位置(可跳過)
     - 點擊按鈕的左上角和右下角來框選區域
     - 確認選取的區域是否正確
   
   - **步驟三**：校準亮度
     - 分別擷取按鈕的明亮狀態和暗淡狀態
     - 系統會自動計算最佳閾值

> 注意：除非刪除特定檔案(settings.json)，或是調整顯示設定，否則這個設定只需要執行一次。

---

## 使用方法  

1. 啟動程式：  
   ```bash
   python auto_add_friend.py
   ```  

2. 工具會自動開始連點好友請求按鈕。  

3. 當成功送出好友邀請時，工具會通知你，並結束連點。  

4. 結束程式：
   - 按住 `Delete` 鍵可以正常結束程式(按到停下為止喔!)
   - 按下 `Ctrl+C` 也可以強制結束程式
   
   程式結束時會顯示結束訊息。

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

## 使用場景示範  

下面是一個搶神包時的實際操作影片：  

[**點擊觀看示範影片**](https://youtu.be/To456YkSjUo)  
(影片使用[**雷電模擬器**](https://www.ldplayer.tw/blog/24307.html))

---

## 注意事項  

- **工具適用於 PTCG 的搶好友請求場景**，特別是因好友上限問題無法成功添加的情況。  
- 請確保你搶神包的 ID 是正確的。
- 本工具僅供學術研究及個人使用，請勿進行任何違反遊戲規章的操作。  

- ### 補充註記 for MacOS Sequoia 15 以上版本
  - MacOS 15.0版本開始，Apple修改了關於螢幕錄取用的隱私權政策。
  - 目前Pillow模組尚未對於這個OS版本更新，因此暫時不支援 MacOS Sequoia 15.0 以後的版本。
  - MacOS Monoma 14 (含)之前的版本則沒有這個問題，請放心使用。
  - 須將 `auto_add_friend.py` 中 `for MacOS` 後面的註解取消才能正常使用。

---  

讓這款工具幫助你，從此不再錯過神包的機會！🎉

