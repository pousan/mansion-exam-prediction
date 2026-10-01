#!/usr/bin/env python3
"""
TAC目次完全網羅型（全250問・全50論点）学習Webアプリケーション生成スクリプト
- 8大分類・テーマ別 目次選択ダッシュボード
- LocalStorageによる正誤履歴・弱点・ブックマークの完全永続化
- 「苦手な問題だけを解く」ワンクリック集中復習モード
- 設問文中の赤色インライン打ち消し線（誤りトラップ可視化）
- 正誤対比カード（VS Card）& 条文原本引用 & 合格のツボ
- 消去法ツール（✕ボタン）& キーボードショートカット
"""

import json
import os

INPUT_JSON = "ui/mankan_master_250q.json"
OUTPUT_HTML = "ui/index.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <title>マンション管理士 2026 予想問題演習 | 目次選択＆弱点克服ナビゲーター</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#eef2ff',
                            100: '#e0e7ff',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                            900: '#312e81',
                        }
                    },
                    fontFamily: {
                        sans: ['"Hiragino Sans"', '"Hiragino Kaku Gothic ProN"', '"Noto Sans JP"', 'sans-serif'],
                        mono: ['"SF Mono"', 'Menlo', 'monospace']
                    }
                }
            }
        }
    </script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        * {
            -webkit-tap-highlight-color: transparent;
            touch-action: manipulation;
        }
        .option-card {
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .option-card:hover {
            transform: translateY(-1px);
        }
        .eliminated {
            opacity: 0.45;
            text-decoration: line-through;
            background-color: rgba(241, 245, 249, 0.6);
        }
        .dark .eliminated {
            background-color: rgba(30, 41, 59, 0.6);
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }
        .dark ::-webkit-scrollbar-thumb {
            background: #475569;
        }
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 min-h-screen font-sans flex flex-col antialiased selection:bg-indigo-500 selection:text-white transition-colors duration-200">

    <!-- Top App Bar -->
    <header class="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-4 lg:px-8 py-3 transition-colors">
        <div class="max-w-6xl mx-auto flex items-center justify-between">
            <div class="flex items-center gap-3">
                <button id="header-home-btn" class="flex items-center gap-2.5 text-left group">
                    <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-500 text-white flex items-center justify-center font-bold shadow-md shadow-indigo-500/20 group-hover:scale-105 transition">
                        <i data-lucide="book-marked" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <div class="text-sm lg:text-base font-black tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
                            <span>マンション管理士 2026 予想問題集</span>
                            <span class="text-[11px] bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-300 font-semibold px-2 py-0.5 rounded-full border border-indigo-200 dark:border-indigo-800 hidden sm:inline-block">全50論点網羅</span>
                        </div>
                        <p class="text-xs text-slate-500 dark:text-slate-400">TAC問題集目次完全対応（全250問）</p>
                    </div>
                </button>
            </div>

            <div class="flex items-center gap-2 sm:gap-3">
                <!-- Dashboard return button (visible only in study mode) -->
                <button id="back-to-toc-header-btn" class="hidden px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-bold transition flex items-center gap-1.5">
                    <i data-lucide="layout-grid" class="w-3.5 h-3.5"></i>
                    <span>目次一覧</span>
                </button>

                <!-- Reset history button -->
                <button id="reset-history-btn" class="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-slate-800 transition" title="学習履歴を初期化">
                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                </button>

                <!-- Dark mode toggle -->
                <button id="theme-toggle" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition" title="ダーク/ライトモード切り替え">
                    <i id="theme-icon" data-lucide="moon" class="w-4 h-4"></i>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-1 max-w-6xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">

        <!-- ========================================== -->
        <!-- VIEW 1: 目次ダッシュボード（テーマ選択画面） -->
        <!-- ========================================== -->
        <div id="view-dashboard" class="space-y-6">

            <!-- Learning Status Overview Card -->
            <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 sm:p-7 shadow-sm space-y-5">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-5">
                    <div>
                        <span class="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">Overall Progress</span>
                        <h2 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white mt-0.5">学習進捗と弱点ステータス</h2>
                    </div>
                    <!-- Quick stats pill -->
                    <div class="flex items-center gap-2 sm:gap-3 flex-wrap text-xs font-bold">
                        <div class="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                            演習済: <span id="stat-answered" class="text-indigo-600 dark:text-indigo-400 font-extrabold text-sm">0</span> / 250問
                        </div>
                        <div class="px-3 py-1.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                            正解率: <span id="stat-accuracy" class="font-extrabold text-sm">0%</span> (<span id="stat-correct">0</span>問)
                        </div>
                        <div class="px-3 py-1.5 rounded-xl bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
                            苦手: <span id="stat-incorrect" class="font-extrabold text-sm">0</span>問
                        </div>
                        <div class="px-3 py-1.5 rounded-xl bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                            保存: <span id="stat-bookmarked" class="font-extrabold text-sm">0</span>問
                        </div>
                    </div>
                </div>

                <!-- Overall Progress Bar -->
                <div class="space-y-1.5">
                    <div class="flex items-center justify-between text-xs text-slate-500 font-semibold">
                        <span>全250問の達成度</span>
                        <span id="stat-progress-percent">0%</span>
                    </div>
                    <div class="h-3 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden flex">
                        <div id="bar-correct" class="bg-emerald-500 transition-all duration-500" style="width: 0%"></div>
                        <div id="bar-incorrect" class="bg-rose-500 transition-all duration-500" style="width: 0%"></div>
                    </div>
                </div>

                <!-- Quick Action Buttons -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
                    <button id="btn-practice-weakness" disabled class="px-4 py-3 rounded-2xl bg-gradient-to-r from-rose-500 to-rose-600 hover:from-rose-600 hover:to-rose-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-extrabold text-xs sm:text-sm shadow-md shadow-rose-500/20 transition flex items-center justify-center gap-2">
                        <i data-lucide="flame" class="w-4 h-4"></i>
                        <span>苦手な問題だけを解く (<span id="btn-weakness-count">0</span>問)</span>
                    </button>
                    <button id="btn-practice-bookmarked" disabled class="px-4 py-3 rounded-2xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-extrabold text-xs sm:text-sm shadow-md shadow-amber-500/20 transition flex items-center justify-center gap-2">
                        <i data-lucide="star" class="w-4 h-4"></i>
                        <span>ブックマーク問題を解く (<span id="btn-bookmarked-count">0</span>問)</span>
                    </button>
                    <button id="btn-practice-unanswered" class="px-4 py-3 rounded-2xl bg-slate-900 hover:bg-slate-800 dark:bg-slate-800 dark:hover:bg-slate-700 text-white font-extrabold text-xs sm:text-sm shadow-md transition flex items-center justify-center gap-2">
                        <i data-lucide="sparkles" class="w-4 h-4 text-indigo-400"></i>
                        <span>未着手の問題を解く (<span id="btn-unanswered-count">105</span>問)</span>
                    </button>
                </div>
            </div>

            <!-- Categories Accordion Container -->
            <div class="space-y-4">
                <div class="flex items-center justify-between px-1">
                    <h3 class="text-sm font-extrabold text-slate-500 uppercase tracking-wider flex items-center gap-2">
                        <i data-lucide="layers" class="w-4 h-4"></i>
                        <span>目次から問題の種類（分野・テーマ）を選択</span>
                    </h3>
                    <button id="toggle-all-categories" class="text-xs text-indigo-600 dark:text-indigo-400 font-bold hover:underline">
                        すべて開く / 閉じる
                    </button>
                </div>

                <div id="categories-container" class="space-y-4">
                    <!-- Dynamically populated category accordions -->
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- VIEW 2: テーマ別集中演習画面（問題解答画面） -->
        <!-- ========================================== -->
        <div id="view-study" class="hidden space-y-6">

            <!-- Breadcrumb Navigation Bar -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 px-4 py-3 shadow-sm">
                <div class="flex items-center gap-2 text-xs sm:text-sm font-bold text-slate-600 dark:text-slate-300">
                    <button id="back-to-toc-btn" class="hover:text-indigo-600 flex items-center gap-1 text-indigo-600 dark:text-indigo-400 font-black">
                        <i data-lucide="chevron-left" class="w-4 h-4"></i>
                        <span>目次一覧へ</span>
                    </button>
                    <span class="text-slate-300 dark:text-slate-700">/</span>
                    <span id="study-category-label" class="text-slate-500 truncate max-w-[120px] sm:max-w-none"></span>
                    <span class="text-slate-300 dark:text-slate-700">/</span>
                    <span id="study-theme-label" class="text-slate-900 dark:text-white font-extrabold truncate max-w-[180px] sm:max-w-none"></span>
                </div>

                <div class="flex items-center gap-2 self-end sm:self-auto">
                    <!-- Bookmark button -->
                    <button id="study-bookmark-btn" class="px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs font-bold transition flex items-center gap-1.5 hover:bg-slate-50 dark:hover:bg-slate-800">
                        <i id="bookmark-icon" data-lucide="star" class="w-3.5 h-3.5 text-slate-400"></i>
                        <span id="bookmark-text">保存する</span>
                    </button>
                    <!-- Question Index Chips in Current Theme -->
                    <div id="theme-question-chips" class="flex items-center gap-1.5">
                        <!-- Chips dynamically generated -->
                    </div>
                </div>
            </div>

            <!-- Weakness Alert Banner (If answered wrong before) -->
            <div id="weakness-alert-banner" class="hidden rounded-2xl p-4 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 flex items-center gap-3 text-rose-900 dark:text-rose-200 text-xs sm:text-sm shadow-sm animate-pulse">
                <div class="p-2 rounded-xl bg-rose-600 text-white shrink-0">
                    <i data-lucide="alert-triangle" class="w-4 h-4"></i>
                </div>
                <div>
                    <span class="font-extrabold">【⚠️ 過去に不正解だった苦手問題です】</span>
                    <span class="opacity-90">前回の選択: 肢 <span id="prev-choice-label">-</span> ➔ トラップに注意してリベンジしましょう！</span>
                </div>
            </div>

            <!-- Question Card -->
            <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 sm:p-7 shadow-sm space-y-4">
                <!-- Badges -->
                <div class="flex flex-wrap items-center gap-2 text-xs">
                    <span id="q-dept" class="px-2.5 py-1 rounded-md font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"></span>
                    <span id="q-ronten" class="px-2.5 py-1 rounded-md font-bold bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 flex items-center gap-1.5">
                        <i data-lucide="tag" class="w-3.5 h-3.5"></i>
                        <span id="q-ronten-text"></span>
                    </span>
                    <span id="q-rev-badge" class="hidden px-2.5 py-1 rounded-md font-bold bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800 flex items-center gap-1.5 animate-pulse">
                        <i data-lucide="flame" class="w-3.5 h-3.5"></i>
                        <span id="q-rev-text"></span>
                    </span>
                </div>

                <!-- Key Concept Banner (論点の急所) -->
                <div class="bg-gradient-to-r from-indigo-50 via-slate-50 to-white dark:from-indigo-950/40 dark:via-slate-900 dark:to-slate-900 border-l-4 border-indigo-500 rounded-r-xl p-3 sm:p-4">
                    <div class="flex items-start gap-2.5">
                        <div class="p-1 rounded bg-indigo-500 text-white shrink-0 mt-0.5">
                            <i data-lucide="lightbulb" class="w-4 h-4"></i>
                        </div>
                        <div>
                            <div class="text-xs font-bold text-indigo-900 dark:text-indigo-200 tracking-wide uppercase">出題の急所（Key Concept）</div>
                            <p id="q-key-concept" class="text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-200 mt-0.5 leading-relaxed"></p>
                        </div>
                    </div>
                </div>

                <!-- Question Text -->
                <div class="pt-2">
                    <div class="text-xs font-bold text-indigo-600 dark:text-indigo-400 mb-1 flex items-center gap-1.5">
                        <span id="q-number-label">問 1</span>
                        <span class="text-slate-400">/ <span id="q-theme-total-label">1</span></span>
                        <span id="q-id-label" class="text-slate-400 font-mono text-[11px]">(GM-001)</span>
                    </div>
                    <p id="q-text" class="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-relaxed tracking-wide"></p>
                </div>
            </div>

            <!-- Options Card -->
            <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 sm:p-7 shadow-sm space-y-4">
                <div class="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 border-b border-slate-100 dark:border-slate-800 pb-3">
                    <div class="flex items-center gap-2">
                        <i data-lucide="help-circle" class="w-4 h-4 text-indigo-500"></i>
                        <span>解答を選択してください（キーボード 1〜4 キー対応）</span>
                    </div>
                    <span class="text-[11px] bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded font-mono">消去法（✕）対応</span>
                </div>

                <div id="options-container" class="space-y-3">
                    <!-- Options populated here -->
                </div>

                <!-- Action Bar -->
                <div class="pt-4 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-slate-100 dark:border-slate-800">
                    <div class="text-xs text-slate-400 flex items-center gap-1.5">
                        <i data-lucide="info" class="w-3.5 h-3.5"></i>
                        <span>各肢右の「✕」ボタンで消去法（打消し線）を引けます</span>
                    </div>
                    <button id="submit-btn" disabled class="w-full sm:w-auto px-7 py-3 rounded-2xl font-bold text-sm bg-indigo-600 hover:bg-indigo-700 active:scale-95 disabled:bg-slate-200 dark:disabled:bg-slate-800 disabled:text-slate-400 disabled:cursor-not-allowed text-white shadow-md shadow-indigo-600/20 transition flex items-center justify-center gap-2">
                        <span>この肢で回答する</span>
                        <i data-lucide="check-circle-2" class="w-4 h-4"></i>
                    </button>
                </div>
            </div>

            <!-- Feedback & Explanation Card -->
            <div id="explanation-container" class="hidden space-y-6">
                <!-- Result Banner -->
                <div id="result-banner" class="rounded-3xl p-5 border flex items-center justify-between shadow-sm">
                    <!-- Populated dynamically -->
                </div>

                <!-- Detailed Explanation Cards -->
                <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 sm:p-7 shadow-sm space-y-5">
                    <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                        <h3 class="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white flex items-center gap-2">
                            <i data-lucide="book-open-check" class="w-5 h-5 text-indigo-500"></i>
                            <span>肢別詳細解説 & 誤りハイライト対比</span>
                        </h3>
                        <span class="text-xs text-indigo-600 dark:text-indigo-400 font-bold bg-indigo-50 dark:bg-indigo-950 px-2.5 py-1 rounded-full">
                            全4肢の急所を網羅
                        </span>
                    </div>

                    <div id="explanation-cards" class="space-y-4">
                        <!-- Populated dynamically -->
                    </div>
                </div>

                <!-- Bottom Navigation Bar -->
                <div class="flex items-center justify-between pt-2">
                    <button id="prev-btn" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 font-semibold text-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition flex items-center gap-2">
                        <i data-lucide="arrow-left" class="w-4 h-4"></i>
                        <span>前の問題</span>
                    </button>
                    <button id="retry-btn" class="px-4 py-2 rounded-xl text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 text-xs font-semibold hover:bg-slate-100 dark:hover:bg-slate-800 transition flex items-center gap-1.5">
                        <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
                        <span>もう一度解く</span>
                    </button>
                    <button id="next-btn" class="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-600/20 transition flex items-center gap-2">
                        <span>次の問題へ</span>
                        <i data-lucide="arrow-right" class="w-4 h-4"></i>
                    </button>
                </div>
            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="mt-auto border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-6 text-center text-xs text-slate-500 dark:text-slate-400">
        <p>2026年マンション管理士試験 予想問題演習システム (TAC目次完全網羅版・全250問)</p>
        <p class="mt-1 text-slate-400 dark:text-slate-600">区分所有法等改正（令和8年4月1日施行）・標準管理規約・適正化法完全準拠</p>
    </footer>

    <!-- App JavaScript Logic -->
    <script>
        const MASTER_CATEGORIES = %MASTER_JSON%;

        // Flatten all questions with lookup
        const ALL_QUESTIONS = [];
        const Q_MAP = {};
        MASTER_CATEGORIES.forEach(cat => {
            cat.themes.forEach(theme => {
                theme.questions.forEach(q => {
                    q.categoryId = cat.category_id;
                    q.categoryName = cat.category_name;
                    q.themeId = theme.theme_id;
                    q.themeName = theme.theme_name;
                    ALL_QUESTIONS.push(q);
                    Q_MAP[q.id] = q;
                });
            });
        });

        // LocalStorage Keys
        const STORAGE_KEY_HISTORY = 'mankan2026_history';
        const STORAGE_KEY_BOOKMARKS = 'mankan2026_bookmarks';
        const STORAGE_KEY_ELIMINATION = 'mankan2026_elimination';

        // State
        let userHistory = loadStorage(STORAGE_KEY_HISTORY, {}); // { [qid]: { status: 'correct'|'incorrect', choice: num, date: str } }
        let userBookmarks = loadStorage(STORAGE_KEY_BOOKMARKS, {}); // { [qid]: boolean }
        let userEliminations = loadStorage(STORAGE_KEY_ELIMINATION, {}); // { [qid]: { [optNum]: true } }

        // Current Active Study Session
        let currentQueue = []; // Array of Question Objects
        let currentQueueIdx = 0;
        let selectedOptionNum = null;

        // DOM References
        const viewDashboard = document.getElementById('view-dashboard');
        const viewStudy = document.getElementById('view-study');
        const categoriesContainer = document.getElementById('categories-container');
        const backToTocHeaderBtn = document.getElementById('back-to-toc-header-btn');
        const backToTocBtn = document.getElementById('back-to-toc-btn');
        const headerHomeBtn = document.getElementById('header-home-btn');

        // Stats Elements
        const statAnswered = document.getElementById('stat-answered');
        const statAccuracy = document.getElementById('stat-accuracy');
        const statCorrect = document.getElementById('stat-correct');
        const statIncorrect = document.getElementById('stat-incorrect');
        const statBookmarked = document.getElementById('stat-bookmarked');
        const statProgressPercent = document.getElementById('stat-progress-percent');
        const barCorrect = document.getElementById('bar-correct');
        const barIncorrect = document.getElementById('bar-incorrect');

        // Quick practice buttons
        const btnPracticeWeakness = document.getElementById('btn-practice-weakness');
        const btnPracticeBookmarked = document.getElementById('btn-practice-bookmarked');
        const btnPracticeUnanswered = document.getElementById('btn-practice-unanswered');
        const btnWeaknessCount = document.getElementById('btn-weakness-count');
        const btnBookmarkedCount = document.getElementById('btn-bookmarked-count');
        const btnUnansweredCount = document.getElementById('btn-unanswered-count');
        const resetHistoryBtn = document.getElementById('reset-history-btn');

        // Study View Elements
        const studyCategoryLabel = document.getElementById('study-category-label');
        const studyThemeLabel = document.getElementById('study-theme-label');
        const studyBookmarkBtn = document.getElementById('study-bookmark-btn');
        const bookmarkIcon = document.getElementById('bookmark-icon');
        const bookmarkText = document.getElementById('bookmark-text');
        const themeQuestionChips = document.getElementById('theme-question-chips');
        const weaknessAlertBanner = document.getElementById('weakness-alert-banner');
        const prevChoiceLabel = document.getElementById('prev-choice-label');

        const qDept = document.getElementById('q-dept');
        const qRonten = document.getElementById('q-ronten-text');
        const qRevBadge = document.getElementById('q-rev-badge');
        const qRevText = document.getElementById('q-rev-text');
        const qKeyConcept = document.getElementById('q-key-concept');
        const qNumberLabel = document.getElementById('q-number-label');
        const qThemeTotalLabel = document.getElementById('q-theme-total-label');
        const qIdLabel = document.getElementById('q-id-label');
        const qText = document.getElementById('q-text');

        const optionsContainer = document.getElementById('options-container');
        const submitBtn = document.getElementById('submit-btn');

        const explanationContainer = document.getElementById('explanation-container');
        const resultBanner = document.getElementById('result-banner');
        const explanationCards = document.getElementById('explanation-cards');

        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const retryBtn = document.getElementById('retry-btn');

        // Theme management
        const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
        }
        themeToggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            updateThemeIcon();
        });
        function updateThemeIcon() {
            const isDark = document.documentElement.classList.contains('dark');
            themeIcon.setAttribute('data-lucide', isDark ? 'sun' : 'moon');
            lucide.createIcons();
        }

        // Storage helpers
        function loadStorage(key, fallback) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : fallback;
            } catch (e) {
                return fallback;
            }
        }
        function saveStorage(key, val) {
            try {
                localStorage.setItem(key, JSON.stringify(val));
            } catch (e) {}
        }

        // Reset history
        resetHistoryBtn.addEventListener('click', () => {
            if (confirm('これまでの学習履歴（正解・不正解・ブックマーク）をすべて初期化しますか？')) {
                userHistory = {};
                userBookmarks = {};
                userEliminations = {};
                saveStorage(STORAGE_KEY_HISTORY, userHistory);
                saveStorage(STORAGE_KEY_BOOKMARKS, userBookmarks);
                saveStorage(STORAGE_KEY_ELIMINATION, userEliminations);
                updateDashboardStats();
                renderCategoriesDashboard();
                showDashboard();
            }
        });

        // Init Application
        function init() {
            updateThemeIcon();
            updateDashboardStats();
            renderCategoriesDashboard();

            // Keyboard shortcut support in study mode
            window.addEventListener('keydown', (e) => {
                if (viewStudy.classList.contains('hidden')) return;

                if (['1', '2', '3', '4'].includes(e.key)) {
                    selectOption(parseInt(e.key));
                } else if (e.key === 'Enter') {
                    if (!submitBtn.disabled && explanationContainer.classList.contains('hidden')) {
                        submitAnswer();
                    } else if (!explanationContainer.classList.contains('hidden') && currentQueueIdx < currentQueue.length - 1) {
                        loadQuestionInQueue(currentQueueIdx + 1);
                    }
                } else if (e.key === 'ArrowLeft') {
                    if (currentQueueIdx > 0) loadQuestionInQueue(currentQueueIdx - 1);
                } else if (e.key === 'ArrowRight') {
                    if (currentQueueIdx < currentQueue.length - 1) loadQuestionInQueue(currentQueueIdx + 1);
                }
            });

            // Navigation clicks
            backToTocBtn.addEventListener('click', showDashboard);
            backToTocHeaderBtn.addEventListener('click', showDashboard);
            headerHomeBtn.addEventListener('click', showDashboard);

            // Quick practice buttons
            btnPracticeWeakness.addEventListener('click', startWeaknessPractice);
            btnPracticeBookmarked.addEventListener('click', startBookmarkedPractice);
            btnPracticeUnanswered.addEventListener('click', startUnansweredPractice);

            // Toggle all categories
            let allOpen = true;
            document.getElementById('toggle-all-categories').addEventListener('click', () => {
                allOpen = !allOpen;
                document.querySelectorAll('.cat-content').forEach(el => {
                    el.classList.toggle('hidden', !allOpen);
                });
                document.querySelectorAll('.cat-arrow').forEach(el => {
                    el.style.transform = allOpen ? 'rotate(180deg)' : 'rotate(0deg)';
                });
            });
        }

        // Show Views
        function showDashboard() {
            viewDashboard.classList.remove('hidden');
            viewStudy.classList.add('hidden');
            backToTocHeaderBtn.classList.add('hidden');
            updateDashboardStats();
            renderCategoriesDashboard();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function showStudy() {
            viewDashboard.classList.add('hidden');
            viewStudy.classList.remove('hidden');
            backToTocHeaderBtn.classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Update Dashboard Statistics
        function updateDashboardStats() {
            const totalQ = ALL_QUESTIONS.length;
            let correct = 0;
            let incorrect = 0;

            Object.values(userHistory).forEach(h => {
                if (h.status === 'correct') correct++;
                else if (h.status === 'incorrect') incorrect++;
            });

            const answered = correct + incorrect;
            const bookmarked = Object.values(userBookmarks).filter(Boolean).length;
            const unanswered = totalQ - answered;
            const accuracy = answered > 0 ? Math.round((correct / answered) * 100) : 0;

            statAnswered.innerText = answered;
            statCorrect.innerText = correct;
            statIncorrect.innerText = incorrect;
            statAccuracy.innerText = `${accuracy}%`;
            statBookmarked.innerText = bookmarked;

            // Bar updates
            const correctPercent = (correct / totalQ) * 100;
            const incorrectPercent = (incorrect / totalQ) * 100;
            barCorrect.style.width = `${correctPercent}%`;
            barIncorrect.style.width = `${incorrectPercent}%`;
            statProgressPercent.innerText = `${Math.round(((answered) / totalQ) * 100)}% 完了`;

            // Quick button labels
            btnWeaknessCount.innerText = incorrect;
            btnPracticeWeakness.disabled = incorrect === 0;

            btnBookmarkedCount.innerText = bookmarked;
            btnPracticeBookmarked.disabled = bookmarked === 0;

            btnUnansweredCount.innerText = unanswered;
        }

        // Render Categories and Themes Accordions
        function renderCategoriesDashboard() {
            categoriesContainer.innerHTML = '';

            MASTER_CATEGORIES.forEach(cat => {
                // Calculate category stats
                let catTotal = 0;
                let catCorrect = 0;
                let catIncorrect = 0;

                cat.themes.forEach(theme => {
                    theme.questions.forEach(q => {
                        catTotal++;
                        const h = userHistory[q.id];
                        if (h) {
                            if (h.status === 'correct') catCorrect++;
                            else if (h.status === 'incorrect') catIncorrect++;
                        }
                    });
                });

                const catAnswered = catCorrect + catIncorrect;
                const catAccuracy = catAnswered > 0 ? Math.round((catCorrect / catAnswered) * 100) : null;

                // Category Card
                const catDiv = document.createElement('div');
                catDiv.className = 'rounded-3xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden shadow-sm transition';

                // Header
                const header = document.createElement('div');
                header.className = 'p-5 sm:p-6 flex items-center justify-between cursor-pointer select-none hover:bg-slate-50 dark:hover:bg-slate-800/50 transition';
                
                header.innerHTML = `
                    <div class="flex items-center gap-3.5">
                        <div class="w-10 h-10 rounded-2xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center font-bold shrink-0">
                            <i data-lucide="${cat.category_icon || 'book'}" class="w-5 h-5"></i>
                        </div>
                        <div>
                            <div class="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white flex items-center gap-2">
                                <span>${cat.category_name}</span>
                                <span class="text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-semibold">${catTotal}問</span>
                                ${catAccuracy !== null && catAccuracy < 60 ? '<span class="text-[11px] font-bold text-rose-600 bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-900 px-2 py-0.5 rounded-full">⚠️ 苦手分野</span>' : ''}
                            </div>
                            <div class="text-xs text-slate-400 mt-0.5 flex items-center gap-2">
                                <span>正答数: ${catCorrect}/${catTotal}</span>
                                ${catAccuracy !== null ? `<span>(正答率: ${catAccuracy}%)</span>` : '<span>(未解答)</span>'}
                            </div>
                        </div>
                    </div>

                    <div class="flex items-center gap-3">
                        <div class="w-24 sm:w-32 h-2.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden flex">
                            <div class="bg-emerald-500" style="width: ${(catCorrect/catTotal)*100}%"></div>
                            <div class="bg-rose-500" style="width: ${(catIncorrect/catTotal)*100}%"></div>
                        </div>
                        <i data-lucide="chevron-down" class="cat-arrow w-5 h-5 text-slate-400 transition-transform duration-200"></i>
                    </div>
                `;

                // Content (Themes List)
                const content = document.createElement('div');
                content.className = 'cat-content border-t border-slate-100 dark:border-slate-800 p-4 sm:p-6 bg-slate-50/50 dark:bg-slate-950/30 grid grid-cols-1 md:grid-cols-2 gap-3.5';

                cat.themes.forEach(theme => {
                    let thTotal = theme.questions.length;
                    let thCorrect = 0;
                    let thIncorrect = 0;

                    theme.questions.forEach(q => {
                        const h = userHistory[q.id];
                        if (h) {
                            if (h.status === 'correct') thCorrect++;
                            else if (h.status === 'incorrect') thIncorrect++;
                        }
                    });

                    const thAnswered = thCorrect + thIncorrect;
                    let statusBadge = '';
                    if (thAnswered === 0) {
                        statusBadge = `<span class="px-2 py-0.5 rounded-md text-[11px] font-bold bg-slate-100 dark:bg-slate-800 text-slate-500">⚪ 未着手</span>`;
                    } else if (thCorrect === thTotal) {
                        statusBadge = `<span class="px-2 py-0.5 rounded-md text-[11px] font-bold bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300">⭕ 完全制覇 (${thCorrect}/${thTotal})</span>`;
                    } else {
                        statusBadge = `<span class="px-2 py-0.5 rounded-md text-[11px] font-bold bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300">❌ 要復習 (${thIncorrect}問不正解)</span>`;
                    }

                    const themeCard = document.createElement('div');
                    themeCard.className = 'p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-indigo-400 dark:hover:border-indigo-600 transition shadow-sm flex flex-col justify-between gap-3 group cursor-pointer';
                    
                    themeCard.innerHTML = `
                        <div>
                            <div class="flex items-center justify-between gap-2 mb-1.5">
                                <span class="text-[11px] font-bold font-mono px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">${theme.ronten_id}</span>
                                ${statusBadge}
                            </div>
                            <h4 class="font-extrabold text-sm sm:text-base text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition leading-snug">
                                ${theme.theme_name}
                            </h4>
                        </div>
                        <div class="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-100 dark:border-slate-800">
                            <span>収録: ${thTotal}問</span>
                            <span class="font-bold text-indigo-600 dark:text-indigo-400 flex items-center gap-1">
                                <span>このテーマを解く</span>
                                <i data-lucide="arrow-right" class="w-3.5 h-3.5 group-hover:translate-x-0.5 transition"></i>
                            </span>
                        </div>
                    `;

                    themeCard.addEventListener('click', () => {
                        startThemePractice(theme);
                    });

                    content.appendChild(themeCard);
                });

                // Toggle click
                header.addEventListener('click', () => {
                    const isHidden = content.classList.toggle('hidden');
                    const arrow = header.querySelector('.cat-arrow');
                    arrow.style.transform = isHidden ? 'rotate(0deg)' : 'rotate(180deg)';
                });

                catDiv.appendChild(header);
                catDiv.appendChild(content);
                categoriesContainer.appendChild(catDiv);
            });

            lucide.createIcons();
        }

        // Start Practice for a Theme
        function startThemePractice(theme) {
            currentQueue = [...theme.questions];
            currentQueueIdx = 0;
            studyCategoryLabel.innerText = theme.questions[0].categoryName;
            studyThemeLabel.innerText = theme.theme_name;
            showStudy();
            loadQuestionInQueue(0);
        }

        // Start Weakness Practice
        function startWeaknessPractice() {
            const list = ALL_QUESTIONS.filter(q => userHistory[q.id] && userHistory[q.id].status === 'incorrect');
            if (list.length === 0) return;
            currentQueue = list;
            currentQueueIdx = 0;
            studyCategoryLabel.innerText = '集中特訓';
            studyThemeLabel.innerText = `🔥 苦手問題集中復習 (${list.length}問)`;
            showStudy();
            loadQuestionInQueue(0);
        }

        // Start Bookmarked Practice
        function startBookmarkedPractice() {
            const list = ALL_QUESTIONS.filter(q => userBookmarks[q.id]);
            if (list.length === 0) return;
            currentQueue = list;
            currentQueueIdx = 0;
            studyCategoryLabel.innerText = '集中特訓';
            studyThemeLabel.innerText = `⭐ ブックマーク問題 (${list.length}問)`;
            showStudy();
            loadQuestionInQueue(0);
        }

        // Start Unanswered Practice
        function startUnansweredPractice() {
            const list = ALL_QUESTIONS.filter(q => !userHistory[q.id]);
            if (list.length === 0) {
                alert('すべての問題をすでに一度解いています！');
                return;
            }
            currentQueue = list;
            currentQueueIdx = 0;
            studyCategoryLabel.innerText = '未着手問題';
            studyThemeLabel.innerText = `⚪ 未着手演習 (${list.length}問)`;
            showStudy();
            loadQuestionInQueue(0);
        }

        // Load Question in Queue
        function loadQuestionInQueue(idx) {
            currentQueueIdx = idx;
            const q = currentQueue[idx];
            selectedOptionNum = null;

            // Render Theme Question Chips
            renderQueueChips();

            // Bookmark button state
            updateBookmarkButton(q.id);

            // Weakness Alert Banner Check
            const prevHistory = userHistory[q.id];
            if (prevHistory && prevHistory.status === 'incorrect') {
                weaknessAlertBanner.classList.remove('hidden');
                prevChoiceLabel.innerText = prevHistory.choice || '-';
            } else {
                weaknessAlertBanner.classList.add('hidden');
            }

            // Populate Metadata
            qDept.innerText = q.dept;
            qRonten.innerText = `${q.ronten_id} ${q.ronten_name}`;
            if (q.rev_id) {
                qRevBadge.classList.remove('hidden');
                qRevText.innerText = `🔥 2026年改正 (${q.rev_id})`;
            } else {
                qRevBadge.classList.add('hidden');
            }

            qKeyConcept.innerText = q.key_concept;
            qNumberLabel.innerText = `問 ${idx + 1}`;
            qThemeTotalLabel.innerText = currentQueue.length;
            qIdLabel.innerText = `(${q.id})`;
            qText.innerText = q.question;

            // Render Options
            renderOptions();

            // Check if already answered in this session or in history
            const hist = userHistory[q.id];
            if (hist) {
                selectedOptionNum = hist.choice;
                showExplanation();
            } else {
                explanationContainer.classList.add('hidden');
                submitBtn.disabled = true;
            }

            // Navigation Buttons
            prevBtn.disabled = idx === 0;
            prevBtn.classList.toggle('opacity-50', idx === 0);
            prevBtn.classList.toggle('cursor-not-allowed', idx === 0);

            nextBtn.innerHTML = idx === currentQueue.length - 1
                ? `<span>演習完了（目次へ）</span><i data-lucide="check" class="w-4 h-4"></i>`
                : `<span>次の問題へ</span><i data-lucide="arrow-right" class="w-4 h-4"></i>`;

            lucide.createIcons();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Render Queue Chips
        function renderQueueChips() {
            themeQuestionChips.innerHTML = '';
            currentQueue.forEach((q, idx) => {
                const btn = document.createElement('button');
                btn.className = `w-7 h-7 rounded-lg text-xs font-bold transition flex items-center justify-center border `;
                const hist = userHistory[q.id];
                const isCurrent = idx === currentQueueIdx;

                if (isCurrent) {
                    btn.classList.add('ring-2', 'ring-indigo-500', 'ring-offset-1', 'dark:ring-offset-slate-900');
                }

                if (!hist) {
                    btn.classList.add('bg-white', 'dark:bg-slate-800', 'text-slate-600', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
                } else if (hist.status === 'correct') {
                    btn.classList.add('bg-emerald-500', 'text-white', 'border-emerald-600');
                } else {
                    btn.classList.add('bg-rose-500', 'text-white', 'border-rose-600');
                }

                btn.innerText = idx + 1;
                btn.addEventListener('click', () => loadQuestionInQueue(idx));
                themeQuestionChips.appendChild(btn);
            });
        }

        // Bookmark Toggle
        studyBookmarkBtn.addEventListener('click', () => {
            const q = currentQueue[currentQueueIdx];
            userBookmarks[q.id] = !userBookmarks[q.id];
            saveStorage(STORAGE_KEY_BOOKMARKS, userBookmarks);
            updateBookmarkButton(q.id);
            updateDashboardStats();
        });

        function updateBookmarkButton(qid) {
            const isBookmarked = !!userBookmarks[qid];
            if (isBookmarked) {
                studyBookmarkBtn.classList.add('bg-amber-50', 'dark:bg-amber-950/40', 'border-amber-300', 'text-amber-700', 'dark:text-amber-300');
                bookmarkIcon.classList.add('fill-amber-400', 'text-amber-500');
                bookmarkText.innerText = '保存中';
            } else {
                studyBookmarkBtn.classList.remove('bg-amber-50', 'dark:bg-amber-950/40', 'border-amber-300', 'text-amber-700', 'dark:text-amber-300');
                bookmarkIcon.classList.remove('fill-amber-400', 'text-amber-500');
                bookmarkText.innerText = '保存する';
            }
            lucide.createIcons();
        }

        // Render Options
        function renderOptions() {
            optionsContainer.innerHTML = '';
            const q = currentQueue[currentQueueIdx];
            const hist = userHistory[q.id];
            const answered = !!hist;

            if (!userEliminations[q.id]) {
                userEliminations[q.id] = {};
            }

            q.options.forEach((opt) => {
                const optNum = opt.num;
                const isSelected = selectedOptionNum === optNum;
                const isCorrect = optNum === q.answer;
                const isEliminated = !!userEliminations[q.id][optNum];

                const card = document.createElement('div');
                card.className = `option-card relative rounded-2xl border p-4 transition cursor-pointer select-none flex items-start justify-between gap-4 `;

                if (!answered) {
                    if (isSelected) {
                        card.classList.add('border-indigo-600', 'bg-indigo-50/70', 'dark:bg-indigo-950/40', 'ring-2', 'ring-indigo-500/20');
                    } else if (isEliminated) {
                        card.classList.add('eliminated', 'border-slate-200', 'dark:border-slate-800');
                    } else {
                        card.classList.add('border-slate-200', 'dark:border-slate-800', 'bg-white', 'dark:bg-slate-900', 'hover:border-indigo-300');
                    }
                } else {
                    if (isCorrect) {
                        card.classList.add('border-emerald-500', 'bg-emerald-50/70', 'dark:bg-emerald-950/30', 'ring-2', 'ring-emerald-500/20');
                    } else if (isSelected && !isCorrect) {
                        card.classList.add('border-rose-500', 'bg-rose-50/70', 'dark:bg-rose-950/30', 'ring-2', 'ring-rose-500/20');
                    } else {
                        card.classList.add('border-slate-200', 'dark:border-slate-800', 'opacity-70');
                    }
                }

                // Left: Number Badge + Text
                const leftDiv = document.createElement('div');
                leftDiv.className = 'flex items-start gap-3 flex-1';

                const numBadge = document.createElement('span');
                numBadge.className = `w-6 h-6 rounded-lg text-xs font-bold shrink-0 flex items-center justify-center mt-0.5 `;
                if (answered) {
                    if (isCorrect) numBadge.classList.add('bg-emerald-600', 'text-white');
                    else if (isSelected) numBadge.classList.add('bg-rose-600', 'text-white');
                    else numBadge.classList.add('bg-slate-100', 'dark:bg-slate-800', 'text-slate-500');
                } else if (isSelected) {
                    numBadge.classList.add('bg-indigo-600', 'text-white');
                } else {
                    numBadge.classList.add('bg-slate-100', 'dark:bg-slate-800', 'text-slate-600', 'dark:text-slate-400');
                }
                numBadge.innerText = optNum;

                const textSpan = document.createElement('span');
                textSpan.className = `text-sm sm:text-base leading-relaxed ${isSelected ? 'font-semibold text-indigo-950 dark:text-indigo-100' : 'text-slate-700 dark:text-slate-200'}`;
                textSpan.innerText = opt.text;

                leftDiv.appendChild(numBadge);
                leftDiv.appendChild(textSpan);
                card.appendChild(leftDiv);

                // Right: Elimination tools (✕)
                if (!answered) {
                    const toolDiv = document.createElement('div');
                    toolDiv.className = 'flex items-center gap-1 shrink-0';

                    const elimBtn = document.createElement('button');
                    elimBtn.className = `p-1.5 rounded-lg border text-xs transition ${isEliminated ? 'bg-rose-100 border-rose-300 text-rose-700 dark:bg-rose-900/40' : 'border-slate-200 dark:border-slate-700 text-slate-400 hover:text-slate-700'}`;
                    elimBtn.innerHTML = `<i data-lucide="x" class="w-3.5 h-3.5"></i>`;
                    elimBtn.title = '消去線（✕）';
                    elimBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        userEliminations[q.id][optNum] = !isEliminated;
                        saveStorage(STORAGE_KEY_ELIMINATION, userEliminations);
                        renderOptions();
                    });

                    toolDiv.appendChild(elimBtn);
                    card.appendChild(toolDiv);
                }

                // Click select
                if (!answered) {
                    card.addEventListener('click', () => selectOption(optNum));
                }

                optionsContainer.appendChild(card);
            });

            lucide.createIcons();
        }

        function selectOption(num) {
            const q = currentQueue[currentQueueIdx];
            if (userHistory[q.id]) return;
            selectedOptionNum = num;
            submitBtn.disabled = false;
            renderOptions();
        }

        // Submit Answer
        submitBtn.addEventListener('click', submitAnswer);
        function submitAnswer() {
            const q = currentQueue[currentQueueIdx];
            if (selectedOptionNum === null) return;

            const isCorrect = selectedOptionNum === q.answer;
            userHistory[q.id] = {
                status: isCorrect ? 'correct' : 'incorrect',
                choice: selectedOptionNum,
                date: new Date().toISOString()
            };
            saveStorage(STORAGE_KEY_HISTORY, userHistory);

            showExplanation();
            renderQueueChips();
            updateDashboardStats();
            lucide.createIcons();
        }

        // Show Explanation
        function showExplanation() {
            const q = currentQueue[currentQueueIdx];
            const hist = userHistory[q.id];
            const isCorrect = hist.status === 'correct';

            explanationContainer.classList.remove('hidden');

            // Banner
            resultBanner.className = `rounded-3xl p-5 border flex items-center justify-between shadow-sm ${
                isCorrect 
                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800 text-emerald-900 dark:text-emerald-200' 
                : 'bg-rose-50 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800 text-rose-900 dark:text-rose-200'
            }`;

            resultBanner.innerHTML = `
                <div class="flex items-center gap-3.5">
                    <div class="w-10 h-10 rounded-2xl flex items-center justify-center text-white ${isCorrect ? 'bg-emerald-600' : 'bg-rose-600'}">
                        <i data-lucide="${isCorrect ? 'check-circle-2' : 'x-circle'}" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <div class="font-extrabold text-lg flex items-center gap-2">
                            <span>${isCorrect ? '正解です！お見事！' : '不正解…復習して克服しましょう'}</span>
                            <span class="text-xs px-2 py-0.5 rounded-full font-bold ${isCorrect ? 'bg-emerald-200 dark:bg-emerald-800 text-emerald-800 dark:text-emerald-100' : 'bg-rose-200 dark:bg-rose-800 text-rose-800 dark:text-rose-100'}">
                                正解: [ 肢 ${q.answer} ]
                            </span>
                        </div>
                        <div class="text-xs opacity-80 mt-0.5">あなたの選択: 肢 ${hist.choice}</div>
                    </div>
                </div>
            `;

            // 4 Explanation Cards
            explanationCards.innerHTML = '';
            q.options.forEach((opt) => {
                const card = document.createElement('div');
                const isThisCorrect = opt.num === q.answer;
                card.className = `rounded-2xl border p-4 sm:p-5 transition space-y-3.5 ${
                    isThisCorrect 
                    ? 'border-emerald-300 dark:border-emerald-800 bg-emerald-50/30 dark:bg-emerald-950/20' 
                    : 'border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50'
                }`;

                const headerLine = `
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded-md text-xs font-bold ${
                                opt.status === '正' 
                                ? 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200' 
                                : 'bg-rose-100 dark:bg-rose-900/60 text-rose-800 dark:text-rose-200'
                            }">
                                肢 ${opt.num} : 【${opt.status === '正' ? '⭕ 正しい' : '❌ 誤り'}】
                            </span>
                            ${isThisCorrect ? '<span class="text-[11px] font-bold text-emerald-600 bg-emerald-100/70 px-2 py-0.5 rounded">正解肢</span>' : ''}
                        </div>
                        <div class="text-xs text-slate-400 font-mono">${opt.statute}</div>
                    </div>
                `;

                // Highlight and Contrast Section
                let highlightSection = '';
                if (opt.status === '誤' && opt.trap_phrase) {
                    const highlightedOptionText = opt.text.replace(
                        opt.trap_phrase, 
                        `<mark class="bg-rose-200 text-rose-900 dark:bg-rose-900/80 dark:text-rose-100 line-through decoration-rose-600 decoration-2 font-bold px-1.5 py-0.5 rounded">${opt.trap_phrase}</mark>`
                    );

                    highlightSection = `
                        <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs sm:text-sm leading-relaxed">
                            <span class="text-slate-400 font-bold mr-1">設問の文:</span>
                            ${highlightedOptionText}
                        </div>
                        <div class="rounded-xl border border-rose-200 dark:border-rose-900/50 bg-rose-50/60 dark:bg-rose-950/20 p-3.5 space-y-2">
                            <div class="text-[11px] font-bold text-rose-800 dark:text-rose-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-rose-600"></i>
                                <span>誤りの急所（ここがトラップ！）</span>
                            </div>
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                                <div class="bg-white dark:bg-slate-900 p-2.5 rounded-lg border border-rose-100 dark:border-rose-900/30">
                                    <div class="font-bold text-rose-600 dark:text-rose-400 mb-0.5">❌ 問題の記述</div>
                                    <div class="text-slate-700 dark:text-slate-300 font-medium">${opt.trap_phrase}</div>
                                </div>
                                <div class="bg-white dark:bg-slate-900 p-2.5 rounded-lg border border-emerald-100 dark:border-emerald-900/30">
                                    <div class="font-bold text-emerald-600 dark:text-emerald-400 mb-0.5">⭕ 正しい規定</div>
                                    <div class="text-slate-800 dark:text-slate-200 font-bold">${opt.correct_phrase}</div>
                                </div>
                            </div>
                        </div>
                    `;
                }

                const explanationText = `
                    <div class="text-xs sm:text-sm text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
                        ${opt.explanation}
                    </div>
                `;

                const statuteBox = `
                    <div class="bg-slate-100/80 dark:bg-slate-800/60 rounded-xl p-3 text-xs text-slate-600 dark:text-slate-300 space-y-1 border border-slate-200 dark:border-slate-700">
                        <div class="font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                            <i data-lucide="scroll" class="w-3.5 h-3.5 text-indigo-500"></i>
                            <span>条文根拠: ${opt.statute}</span>
                        </div>
                        <div class="italic text-[11px] leading-relaxed pl-4 border-l-2 border-indigo-400 text-slate-700 dark:text-slate-300">${opt.quote}</div>
                    </div>
                `;

                const pointBox = `
                    <div class="text-[11px] text-indigo-700 dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-950/40 px-3 py-1.5 rounded-lg flex items-center gap-1.5 border border-indigo-100 dark:border-indigo-900">
                        <i data-lucide="check" class="w-3.5 h-3.5 text-indigo-500 shrink-0"></i>
                        <span><strong>合格のツボ:</strong> ${opt.key_point}</span>
                    </div>
                `;

                card.innerHTML = headerLine + highlightSection + explanationText + statuteBox + pointBox;
                explanationCards.appendChild(card);
            });

            renderOptions();
        }

        // Retry Question
        retryBtn.addEventListener('click', () => {
            const q = currentQueue[currentQueueIdx];
            delete userHistory[q.id];
            saveStorage(STORAGE_KEY_HISTORY, userHistory);
            loadQuestionInQueue(currentQueueIdx);
            updateDashboardStats();
        });

        // Navigation
        prevBtn.addEventListener('click', () => {
            if (currentQueueIdx > 0) loadQuestionInQueue(currentQueueIdx - 1);
        });
        nextBtn.addEventListener('click', () => {
            if (currentQueueIdx < currentQueue.length - 1) {
                loadQuestionInQueue(currentQueueIdx + 1);
            } else {
                alert('このテーマのすべての問題が完了しました！目次一覧に戻ります。');
                showDashboard();
            }
        });

        // Start
        init();
    </script>
</body>
</html>
"""

def main():
    print(f"Reading master questions JSON from {INPUT_JSON}...")
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    master_json_str = json.dumps(master_data, ensure_ascii=False)
    html_content = HTML_TEMPLATE.replace("%MASTER_JSON%", master_json_str)

    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully generated full Web App HTML at: {OUTPUT_HTML}")
    print(f"File size: {os.path.getsize(OUTPUT_HTML)} bytes")

if __name__ == "__main__":
    main()
