call plug#begin()
  " Themes
  Plug 'dracula/vim'
  Plug 'morhetz/gruvbox'
  Plug 'arcticicestudio/nord-vim'
  
  " Airline
  " Plug 'vim-airline/vim-airline'
  " Plug 'vim-airline/vim-airline-themes'
  
  " Lightline.vim
  Plug 'itchyny/lightline.vim'
  
  " Golang
  Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }
  
  " Typescript
  Plug 'HerringtonDarkholme/yats.vim' " TS Syntax
  
  " Utils
  Plug 'preservim/nerdtree'
  Plug 'tpope/vim-fugitive'
  Plug 'christoomey/vim-tmux-navigator'
  Plug 'ctrlpvim/ctrlp.vim'
  Plug 'sheerun/vim-polyglot'
  Plug 'editorconfig/editorconfig-vim'
  
  " Autocomplete
  " Plug 'Shougo/deoplete.nvim', {'do':':UpdateRemotePlugins'}
  Plug 'neoclide/coc.nvim', {'branch': 'release'}

  " UI
  Plug 'ryanoasis/vim-devicons'

call plug#end()

" Colors
" let g:gruvbox_contrast_dark = 'hard'
set termguicolors
colorscheme gruvbox

" Spaces & Tabs
set tabstop=3       " number of visual spaces per TAB
set softtabstop=3   " number of spaces in tab when editing
set shiftwidth=3    " number of spaces to use for autoindent
set expandtab       " tabs are space
set autoindent
set copyindent      " copy indent from the previous line

" UI Config
set hidden
set showcmd                  " show command in bottom bar
set cursorline               " highlight current line
set wildmenu                 " visual autocomplete for command menu
set showmatch                " highlight matching brace
set laststatus=2             " window will always have a status line
set nobackup
set noswapfile
set relativenumber
set number
set encoding=utf-8
set fileencoding=utf-8
set colorcolumn=80
set noshowmode
set splitright
set splitbelow
autocmd vimenter * set cmdheight=1

" Airline
" let g:airline#extensions#tabline#enabled = 1
" let g:airline#extensions#tabline#buffer_nr_show = 1

" Lightline
let g:lightline = {
      \ 'active': {
      \   'left': [ [ 'mode', 'paste' ],
      \             [ 'gitbranch', 'readonly', 'filename', 'modified' ] ]
      \ },
      \ 'component_function': {
      \   'gitbranch': 'FugitiveHead'
      \ },
      \ }

" Coc Extensions
let g:coc_global_extensions = [
	\ 'coc-snippets',
	\ 'coc-pairs',
	\ 'coc-eslint',
	\ 'coc-emmet',
	\ 'coc-tsserver',
	\ 'coc-json',
	\ 'coc-go',
	\ 'coc-css',
   \ 'coc-python',
   \ 'coc-elixir',
   \ 'coc-rls'
\ ]

" Mappings
nmap <C-g> :NERDTreeToggle<CR>
inoremap jk <ESC>
nnoremap <silent> <space>p :bp<CR>
nnoremap <silent> <space><TAB> :bn<CR>

" ctrlp configs
let g:ctrlp_custom_ignore = '\v[\/](_build|deps|node_modules)|(\.(git|svn|hg))$'

" ctrlp mapping
nnoremap <silent> <space>ff :CtrlP<CR>
nnoremap <silent> <space>fp :CtrlPBuffer<CR>
nnoremap <silent> <space>fa :CtrlPMixed<CR>
vnoremap <silent> <space>ff :CtrlP<CR>
vnoremap <silent> <space>fp :CtrlPBuffer<CR>
vnoremap <silent> <space>fa :CtrlPMixed<CR>

" Providers
let g:python3_host_prog = '/usr/bin/python3' 
let g:loaded_python_provider = 0

" Deoplete
" let g:deoplete#enable_at_startup = 1

" Nerd Tree
" autocmd vimenter * NERDTree
let g:NERDTreeIgnore = ['^node_modules$']

" sync open file with NERDTree
" " Check if NERDTree is open or active
function! IsNERDTreeOpen()        
  return exists("t:NERDTreeBufName") && (bufwinnr(t:NERDTreeBufName) != -1)
endfunction

" Call NERDTreeFind iff NERDTree is active, current window contains a modifiable
" file, and we're not in vimdiff
function! SyncTree()
  if &modifiable && IsNERDTreeOpen() && strlen(expand('%')) > 0 && !&diff
    NERDTreeFind
    wincmd p
  endif
endfunction

" Highlight currently open buffer in NERDTree
autocmd BufEnter * call SyncTree()

" disable vim-go :GoDef short cut (gd)
" this is handled by LanguageClient [LC]
let g:go_def_mapping_enabled = 0

" -------------------------------------------------------------------------------------------------
" coc.nvim default settings
" -------------------------------------------------------------------------------------------------

" if hidden is not set, TextEdit might fail.
set hidden
" Better display for messages
set cmdheight=2
" Smaller updatetime for CursorHold & CursorHoldI
set updatetime=300
" don't give |ins-completion-menu| messages.
set shortmess+=c
" always show signcolumns
set signcolumn=yes

" Use tab for trigger completion with characters ahead and navigate.
" Use command ':verbose imap <tab>' to make sure tab is not mapped by other plugin.
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" Use <c-space> to trigger completion.
inoremap <silent><expr> <c-space> coc#refresh()

" Use `[c` and `]c` to navigate diagnostics
nmap <silent> [c <Plug>(coc-diagnostic-prev)
nmap <silent> ]c <Plug>(coc-diagnostic-next)

" Remap keys for gotos
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Use U to show documentation in preview window
nnoremap <silent> U :call <SID>show_documentation()<CR>

" Remap for rename current word
nmap <leader>rn <Plug>(coc-rename)

" Remap for format selected region
vmap <leader>f  <Plug>(coc-format-selected)
nmap <leader>f  <Plug>(coc-format-selected)
" Show all diagnostics
nnoremap <silent> <space>a  :<C-u>CocList diagnostics<cr>
" Manage extensions
nnoremap <silent> <space>e  :<C-u>CocList extensions<cr>
" Show commands
nnoremap <silent> <space>c  :<C-u>CocList commands<cr>
" Find symbol of current document
nnoremap <silent> <space>o  :<C-u>CocList outline<cr>
" Search workspace symbols
nnoremap <silent> <space>s  :<C-u>CocList -I symbols<cr>
" Do default action for next item.
nnoremap <silent> <space>j  :<C-u>CocNext<CR>
" Do default action for previous item.
nnoremap <silent> <space>k  :<C-u>CocPrev<CR>
" Resume latest coc list
nnoremap <silent> <space>p  :<C-u>CocListResume<CR>
