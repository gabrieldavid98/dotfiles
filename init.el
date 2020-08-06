(global-linum-mode 1)
(electric-pair-mode 1)
(show-paren-mode 1)
(ido-mode 1)

(scroll-bar-mode 0)
(tool-bar-mode 0)
(menu-bar-mode 0)

(setq ido-enable-flex-matching t)
(setq ido-everywhere t)
(setq backup-directory-alist '(("." . "~/emacs.d/backup"))
      backup-by-copying t
      version-control t
      delete-old-versions t
      kept-new-versions 5
      kept-old-versions 5)

(set-default-font "Ubuntu Mono 12" nil t)

(defalias 'list-buffers 'ibuffer)

(require 'package)
(setq package-enable-at-startup nil)
(add-to-list 'package-archives
	     '("melpa" . "https://melpa.org/packages/"))

(package-initialize)

(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))

(use-package try
  :ensure t)

(use-package which-key
  :ensure t
  :config (which-key-mode))

;; (use-package gruvbox-theme
;;   :ensure t
;;   :config (load-theme 'gruvbox t))

(use-package gruber-darker-theme
  :ensure t
  :config (load-theme 'gruber-darker t))

(use-package ace-window
  :ensure t
  :init
  (progn
    (global-set-key [remap other-window] 'ace-window)))

(use-package counsel
  :ensure t)

(use-package ivy
  :ensure t
  :diminish (ivy-mode)
  :bind (("C-x b" . ivy-switch-buffer))
  :config
  (ivy-mode 1)
  (setq ivy-use-virtual-buffers t)
  (setq ivy-display-style 'fancy))

(use-package swiper
  :ensure try
  :bind (("C-s" . swiper)
	 ("C-r" . swiper)
	 ("C-c C-r" . ivy-resume)
	 ("M-x" . counsel-M-x)
	 ("C-x C-f" . counsel-find-file))
  :config
  (progn
    (ivy-mode 1)
    (setq ivy-use-virtual-buffers t)
    (setq enable-recursive-minibuffers t)
    (define-key read-expression-map (kbd "C-r") 'counsel-expression-history)))

(use-package avy
  :ensure t
  :bind ("M-s" . avy-goto-char))

(use-package company
  :ensure t
  :config (add-hook 'after-init-hook 'global-company-mode))

(use-package company-php
  :defer
  :after company)

(use-package web-mode
  :ensure t
  :config
  (add-hook 'web-mode-hook 'my-web-mode-hook)
  (add-to-list 'auto-mode-alist '("\\.html?\\'" . web-mode))
  (add-to-list 'auto-mode-alist '("\\.php\\'" . web-mode))
  (add-to-list 'auto-mode-alist '("\\.eex\\'" . web-mode)))

(setq web-mode-enable-auto-closing t)

(defun my-web-mode-hook ()
  "Hooks for Web mode."
  (setq web-mode-markup-indent-offset 3)
  (setq web-mode-css-indent-offset 3)
  (setq web-mode-code-indent-offset 3)
  (setq web-mode-attr-indent-offset 3))

