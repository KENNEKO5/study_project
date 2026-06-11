
# Git チートシート
---

## 🔧 初期設定
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor "code --wait"
git config --list
```

---

## 📁 リポジトリ作成・取得
```bash
git init
git init my-project
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git
```

---

## 🔍 状態確認・差分
```bash
git status
git diff
git diff --cached
git log
git log --oneline --graph --all
```

---

## ✏️ 追加・コミット
```bash
git add file.txt
git add file1.txt file2.txt
git add .
git commit -m "メッセージ"
git commit -am "変更をまとめてコミット"
```

---

## 🌿 ブランチ操作
```bash
git branch
git branch feature/login
git switch feature/login
git switch -c feature/login
git branch -m new-branch-name
git branch -d feature/login
git branch -D feature/login
```

---

## 🔀 マージ・リベース
```bash
git switch main
git merge feature/login
git status
git switch feature/login
git rebase main
```

---

## 🌐 リモート操作
```bash
git remote -v
git remote add origin https://github.com/user/repo.git
git remote remove origin
git remote rename origin upstream
```

---

## 🚀 プッシュ・プル・フェッチ
```bash
git push -u origin main
git push
git pull
git fetch
git branch -r
```

---

## 🏷️ タグ操作
```bash
git tag v1.0.0
git tag -a v1.0.0 -m "リリース 1.0.0"
git tag
git push origin v1.0.0
git push origin --tags
```

---

## 📦 スタッシュ
```bash
git stash
git stash push -m "作業中の修正"
git stash list
git stash apply
git stash apply stash@{1}
git stash pop
git stash drop stash@{1}
git stash clear
```

---

## ♻️ 取り消し・やり直し
```bash
git restore --staged file.txt
git restore file.txt
git commit --amend -m "新しいメッセージ"
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
git revert <commit-hash>
```

---

## 🚧 新規プロジェクトの流れ
```bash
mkdir my-project
cd my-project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

---

## 🛠️ 開発フロー（ブランチ運用）
```bash
git switch main
git pull
git switch -c feature/some-task
git status
git add .
git commit -m "Implement some task"
git push -u origin feature/some-task
```
