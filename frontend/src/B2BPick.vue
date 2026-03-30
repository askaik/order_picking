<template>
  <div>
    <!-- B2B Workflow Steps Indicator -->
    <div class="flex items-center justify-center gap-2 mb-6 text-xs font-bold uppercase tracking-wider flex-wrap">
      <div :class="stepClass(1)" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-all">
        <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] border" :class="stepNumClass(1)">1</span>
        Pick Items
      </div>
      <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      <div :class="stepClass(2)" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-all">
        <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] border" :class="stepNumClass(2)">2</span>
        Material Request
      </div>
      <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      <div :class="stepClass(3)" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-all">
        <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] border" :class="stepNumClass(3)">3</span>
        Stock Entry
      </div>
      <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      <div :class="stepClass(4)" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-all">
        <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] border" :class="stepNumClass(4)">4</span>
        Complete
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 mb-6 relative overflow-hidden">
      <div class="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-purple-400 to-indigo-500"></div>
      <div class="flex justify-between items-end mb-3">
        <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider flex items-center gap-2">
          <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
          B2B Picking Progress
        </h4>
        <div class="text-2xl font-black" :class="percentage === 100 ? 'text-green-600' : 'text-purple-600'">{{ percentage }}%</div>
      </div>
      <div class="w-full bg-gray-100 rounded-full h-4 mb-2 overflow-hidden shadow-inner ring-1 ring-inset ring-gray-200/50">
        <div class="h-4 rounded-full transition-all duration-500 ease-out relative"
          :class="percentage === 100 ? 'bg-gradient-to-r from-green-400 to-green-500' : 'bg-gradient-to-r from-purple-400 to-indigo-500'"
          :style="{ width: percentage + '%' }">
          <div class="absolute inset-0 bg-white/20 w-full animate-[shimmer_2s_infinite] -skew-x-12 translate-x-[-100%]"></div>
        </div>
      </div>
      <!-- Active SO + Customer -->
      <div class="flex flex-wrap items-center gap-3 mt-4">
        <div v-if="currentSO" class="text-sm font-medium text-gray-500 bg-gray-50 dark:bg-slate-700 dark:text-slate-200 px-3 py-1.5 rounded-md border border-gray-100 dark:border-slate-600 shadow-sm">
          Active: <span class="font-bold text-gray-800 dark:text-white">{{ currentSO }}</span>
        </div>
        <div v-if="customerName" class="text-sm font-medium text-purple-700 bg-purple-50 dark:bg-purple-900/30 dark:text-purple-300 px-3 py-1.5 rounded-md border border-purple-200 dark:border-purple-800 shadow-sm flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          {{ customerName }}
        </div>
        <div v-if="soStatus" class="text-xs font-bold px-2.5 py-1.5 rounded-md uppercase tracking-wider shadow-sm border"
          :class="soStatus === 'To Deliver and Bill' ? 'bg-blue-100 text-blue-700 border-blue-200' : soStatus === 'Completed' ? 'bg-green-100 text-green-700 border-green-200' : 'bg-gray-100 text-gray-700 border-gray-200'">
          {{ soStatus }}
        </div>
        <!-- MR Created badge -->
        <div v-if="mrName" class="text-xs font-bold px-2.5 py-1.5 rounded-md uppercase tracking-wider shadow-sm border bg-amber-100 text-amber-700 border-amber-200">
          MR: {{ mrName }}
        </div>
      </div>
    </div>

    <!-- STEP 1: Scan Inputs -->
    <div v-if="currentStep === 1" class="flex flex-col gap-4 mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1 relative group">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg class="w-6 h-6 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          </div>
          <input v-model="soScan" @keyup.enter="handleSOScan" type="text" id="scan_so_input"
            class="w-full pl-12 pr-4 py-4 text-lg border-2 border-gray-200 dark:border-slate-600 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 transition-all shadow-sm font-medium bg-white dark:bg-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500"
            placeholder="Scan Sales Order Barcode..."
            :disabled="isLoading" ref="soInputRef">
        </div>
        <div class="flex flex-row gap-2 flex-1">
          <div class="flex-1 relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-6 h-6 text-gray-400 group-focus-within:text-indigo-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"/></svg>
            </div>
            <input v-model="itemScan" @keyup.enter="handleItemScan" type="text" id="scan_b2b_item_input"
              :class="{'ring-4 ring-green-400/50 bg-green-50': flashSuccess, 'border-gray-200 focus:border-indigo-500 focus:ring-indigo-500/20': !flashSuccess}"
              class="w-full pl-12 pr-4 py-4 text-lg border-2 rounded-xl focus:ring-4 transition-all shadow-sm font-medium bg-white dark:bg-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 disabled:bg-gray-100 dark:disabled:bg-slate-900 disabled:cursor-not-allowed"
              placeholder="Scan Item Barcode (supports UOM/Box)..."
              :disabled="!currentSO || percentage === 100 || isLoading" ref="itemInputRef">
          </div>
          <!-- Manual Qty Multiplier -->
          <div class="w-24 flex-shrink-0">
            <div class="relative">
              <label class="absolute -top-2 left-2 bg-white dark:bg-slate-800 px-1 text-[10px] font-bold text-purple-600 dark:text-purple-400 uppercase tracking-wider z-10">× Qty</label>
              <input v-model.number="manualQtyMultiplier" type="number" min="1" step="1"
                class="w-full py-4 px-3 text-lg text-center border-2 border-purple-300 dark:border-purple-700 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 transition-all shadow-sm font-black bg-purple-50 dark:bg-purple-900/30 dark:text-purple-200"
                :disabled="!currentSO || percentage === 100 || isLoading">
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Last scanned info -->
    <Transition name="fade">
      <div v-if="lastScanInfo && currentStep === 1" class="mb-4 p-3 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 border border-indigo-200 dark:border-indigo-800 text-sm font-medium text-indigo-700 dark:text-indigo-300 flex items-center gap-2">
        <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        {{ lastScanInfo }}
      </div>
    </Transition>

    <!-- Items Lists (Step 1) -->
    <div v-if="currentStep === 1" class="flex flex-col md:flex-row gap-6 mb-6">
      <!-- Items to Pick -->
      <div class="flex-1 bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 flex flex-col min-h-[350px]">
        <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-4 border-b pb-3 flex justify-between items-center">
          <span class="flex items-center gap-2"><div class="w-2 h-2 rounded-full bg-purple-500"></div> Items to Pick</span>
          <span class="bg-gray-100 text-gray-600 px-2 py-0.5 rounded text-xs">{{ itemsToPick.filter(i => i.qty > 0).length }} pending</span>
        </h4>
        <div class="flex-1 overflow-y-auto pr-2 -mr-2 space-y-2" v-if="itemsToPick.length > 0">
          <div v-for="item in itemsToPick.filter(i => i.qty > 0)" :key="item.item_code"
            class="flex justify-between items-center bg-gray-50 dark:bg-slate-700 border border-gray-100 dark:border-slate-600 p-3 rounded-lg hover:border-purple-200 hover:shadow-sm transition-all group gap-3">
            <div class="flex items-center gap-3 overflow-hidden">
              <div v-if="item.image" class="w-12 h-12 flex-shrink-0 bg-white rounded-md p-1 border border-gray-200 overflow-hidden flex items-center justify-center">
                <img :src="item.image" class="max-w-full max-h-full object-contain" :alt="item.item_code">
              </div>
              <div v-else class="w-12 h-12 flex-shrink-0 bg-gray-100 rounded-md border border-gray-200 flex items-center justify-center text-gray-400">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              </div>
              <div class="flex flex-col overflow-hidden">
                <div class="font-bold text-gray-800 dark:text-slate-100 tracking-wide truncate">{{ item.item_code }}</div>
                <div class="text-xs text-gray-500 truncate" :title="item.item_name">{{ item.item_name || 'No Name' }}</div>
              </div>
            </div>
            <div class="text-lg font-black bg-white dark:bg-slate-800 px-3 py-1 rounded shadow-sm border border-gray-200 group-hover:border-purple-300 group-hover:text-purple-700 transition-colors flex-shrink-0">{{ item.qty }} <span class="text-xs text-gray-400 font-medium">{{ item.uom }}</span></div>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col items-center justify-center text-gray-400 opacity-60">
          <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
          <p class="font-medium text-lg">Scan a Sales Order to begin.</p>
        </div>
      </div>
      <!-- Picked Items -->
      <div class="flex-1 bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 flex flex-col min-h-[350px]">
        <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-4 border-b pb-3 flex justify-between items-center">
          <span class="flex items-center gap-2"><div class="w-2 h-2 rounded-full bg-green-500"></div> Picked Items</span>
          <span class="bg-green-50 text-green-700 px-2 py-0.5 rounded text-xs border border-green-100">{{ pickedItems.reduce((a, o) => a + o.qty, 0) }} total</span>
        </h4>
        <div class="flex-1 overflow-y-auto pr-2 -mr-2 space-y-2" v-if="pickedItems.length > 0">
          <div v-for="item in pickedItems" :key="item.item_code"
            class="flex justify-between items-center bg-green-50 border border-green-100 p-3 rounded-lg shadow-sm gap-3">
            <div class="flex items-center gap-3 overflow-hidden">
              <div v-if="item.image" class="w-10 h-10 flex-shrink-0 bg-white rounded-md border border-green-200 overflow-hidden p-0.5 flex items-center justify-center">
                <img :src="item.image" class="max-w-full max-h-full object-contain" :alt="item.item_code">
              </div>
              <div class="flex flex-col overflow-hidden">
                <div class="font-bold text-green-800 tracking-wide flex items-center gap-1.5 truncate">
                  <svg class="w-4 h-4 text-green-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                  <span class="truncate">{{ item.item_code }}</span>
                </div>
                <div class="text-xs text-green-700/80 truncate" :title="item.item_name">{{ item.item_name || 'No Name' }}</div>
              </div>
            </div>
            <div class="text-lg font-black bg-white text-green-700 px-3 py-1 rounded shadow-sm border border-green-200 flex-shrink-0">{{ item.qty }}</div>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col items-center justify-center text-gray-400 opacity-60">
          <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
          <p class="font-medium">No items picked yet.</p>
        </div>
      </div>
    </div>

    <!-- Print Button (visible during picking when items exist) -->
    <div v-if="currentStep === 1 && pickedItems.length > 0" class="flex justify-end mb-4">
      <button @click="printPickList" class="text-sm font-semibold text-gray-600 bg-gray-100 hover:bg-gray-200 dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600 px-4 py-2 rounded-lg transition-colors shadow-sm ring-1 ring-inset ring-gray-200 dark:ring-slate-600 flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
        Print Pick List
      </button>
    </div>

    <!-- Action: Create Material Request (after 100%) -->
    <div v-if="currentStep === 1 && percentage === 100 && currentSO" class="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 mb-6">
      <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-4 flex items-center gap-2">
        <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
        Create Material Request
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Source Warehouse *</label>
          <select v-model="sourceWarehouse" class="w-full border-2 border-gray-200 rounded-lg px-3 py-2.5 text-sm font-medium focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 bg-white dark:bg-slate-700 dark:border-slate-600 dark:text-slate-100">
            <option value="">Select...</option>
            <option v-for="w in warehouses" :key="w" :value="w">{{ w }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Destination Warehouse *</label>
          <select v-model="targetWarehouse" class="w-full border-2 border-gray-200 rounded-lg px-3 py-2.5 text-sm font-medium focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 bg-white dark:bg-slate-700 dark:border-slate-600 dark:text-slate-100">
            <option value="">Select...</option>
            <option v-for="w in warehouses" :key="w" :value="w">{{ w }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Required By Date *</label>
          <input v-model="requiredByDate" type="date" class="w-full border-2 border-gray-200 rounded-lg px-3 py-2.5 text-sm font-medium focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 bg-white dark:bg-slate-700 dark:border-slate-600 dark:text-slate-100">
        </div>
      </div>
      <button @click="createMR" :disabled="!sourceWarehouse || !targetWarehouse || !requiredByDate || isLoading"
        class="bg-amber-600 hover:bg-amber-700 text-white font-bold py-2.5 px-6 rounded-lg text-sm shadow-md transition-all hover:-translate-y-0.5 hover:shadow-lg flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Create Material Request
      </button>
    </div>

    <!-- STEP 2: Submit Material Request -->
    <div v-if="currentStep === 2" class="bg-white dark:bg-slate-800 p-8 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 mb-6 text-center">
      <div class="flex items-center justify-center w-16 h-16 mx-auto bg-amber-100 text-amber-600 rounded-full mb-4">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
      </div>
      <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Material Request Created</h3>
      <p class="text-gray-500 dark:text-slate-400 mb-1 font-medium">
        <a :href="'/app/material-request/' + mrName" target="_blank" class="text-amber-600 font-bold hover:underline">{{ mrName }}</a>
        has been saved as Draft.
      </p>
      <p class="text-gray-400 dark:text-slate-500 mb-6 text-sm">Please review and submit to proceed with the Material Transfer.</p>
      <button @click="submitMR" :disabled="isLoading"
        class="bg-amber-600 hover:bg-amber-700 text-white font-bold py-3 px-8 rounded-lg text-sm shadow-md transition-all hover:-translate-y-0.5 hover:shadow-lg inline-flex items-center gap-2 disabled:opacity-50">
        <svg v-if="isLoading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/></svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
        Submit Material Request
      </button>
    </div>

    <!-- STEP 3: Create Stock Entry -->
    <div v-if="currentStep === 3" class="bg-white dark:bg-slate-800 p-8 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 mb-6">
      <div class="flex items-center justify-center w-16 h-16 mx-auto bg-green-100 text-green-600 rounded-full mb-4">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
      </div>
      <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2 text-center">Create Material Transfer</h3>
      <p class="text-gray-500 dark:text-slate-400 mb-6 text-center font-medium text-sm">Material Request <span class="font-bold text-amber-600">{{ mrName }}</span> has been submitted. Now create the Stock Entry.</p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Cost Center *</label>
          <select v-model="costCenter" class="w-full border-2 border-gray-200 rounded-lg px-3 py-2.5 text-sm font-medium focus:border-green-500 focus:ring-2 focus:ring-green-500/20 bg-white dark:bg-slate-700 dark:border-slate-600 dark:text-slate-100">
            <option value="">Select...</option>
            <option v-for="cc in costCenters" :key="cc" :value="cc">{{ cc }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Purpose of Transfer</label>
          <input v-model="purposeOfTransfer" type="text" class="w-full border-2 border-gray-200 rounded-lg px-3 py-2.5 text-sm font-medium focus:border-green-500 focus:ring-2 focus:ring-green-500/20 bg-white dark:bg-slate-700 dark:border-slate-600 dark:text-slate-100"
            :placeholder="'Transfer by B2B Order Pick for ' + customerName">
        </div>
      </div>
      <div class="text-center">
        <button @click="createSE" :disabled="!costCenter || isLoading"
          class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg text-sm shadow-md transition-all hover:-translate-y-0.5 hover:shadow-lg inline-flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
          <svg v-if="isLoading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
          Create &amp; Submit Material Transfer
        </button>
      </div>
    </div>

    <!-- STEP 4: Completed Summary -->
    <div v-if="currentStep === 4" class="bg-white dark:bg-slate-800 p-8 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 mb-6">
      <div class="flex items-center justify-center w-16 h-16 mx-auto bg-green-100 text-green-600 rounded-full mb-4">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      </div>
      <h3 class="text-xl font-bold text-green-700 dark:text-green-400 mb-1 text-center">B2B Order Completed!</h3>
      <p class="text-gray-500 dark:text-slate-400 mb-6 text-center text-sm">
        Sales Order <span class="font-bold">{{ completedSE.so_name }}</span> &mdash; {{ completedSE.customer_name }}
      </p>

      <!-- Reference Links -->
      <div class="flex flex-wrap justify-center gap-3 mb-6">
        <a :href="'/app/material-request/' + completedSE.mr_name" target="_blank" class="text-sm font-bold text-amber-700 bg-amber-50 border border-amber-200 px-4 py-2 rounded-lg hover:bg-amber-100 transition-colors flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          MR: {{ completedSE.mr_name }}
        </a>
        <a :href="'/app/stock-entry/' + completedSE.se_name" target="_blank" class="text-sm font-bold text-green-700 bg-green-50 border border-green-200 px-4 py-2 rounded-lg hover:bg-green-100 transition-colors flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
          SE: {{ completedSE.se_name }}
        </a>
      </div>

      <!-- Items Summary Table -->
      <div class="overflow-x-auto mb-6 border border-gray-200 dark:border-slate-600 rounded-lg">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 dark:bg-slate-700">
            <tr>
              <th class="text-left px-4 py-2.5 text-xs font-bold text-gray-500 uppercase">#</th>
              <th class="text-left px-4 py-2.5 text-xs font-bold text-gray-500 uppercase">Item Code</th>
              <th class="text-left px-4 py-2.5 text-xs font-bold text-gray-500 uppercase">Item Name</th>
              <th class="text-right px-4 py-2.5 text-xs font-bold text-gray-500 uppercase">Qty</th>
              <th class="text-left px-4 py-2.5 text-xs font-bold text-gray-500 uppercase">UOM</th>
              <th class="text-left px-4 py-2.5 text-xs font-bold text-gray-500 uppercase">From</th>
              <th class="text-left px-4 py-2.5 text-xs font-bold text-gray-500 uppercase">To</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in completedSE.items" :key="idx" class="border-t border-gray-100 dark:border-slate-600">
              <td class="px-4 py-2 text-gray-400">{{ idx + 1 }}</td>
              <td class="px-4 py-2 font-bold text-gray-700 dark:text-slate-200">{{ item.item_code }}</td>
              <td class="px-4 py-2 text-gray-600 dark:text-slate-300">{{ item.item_name }}</td>
              <td class="px-4 py-2 text-right font-black text-green-700">{{ item.qty }}</td>
              <td class="px-4 py-2 text-gray-500">{{ item.uom }}</td>
              <td class="px-4 py-2 text-gray-500 text-xs">{{ item.from_warehouse }}</td>
              <td class="px-4 py-2 text-gray-500 text-xs">{{ item.to_warehouse }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap justify-center gap-3">
        <button @click="printCompletedSummary" class="text-sm font-semibold text-gray-600 bg-gray-100 hover:bg-gray-200 dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600 px-5 py-2.5 rounded-lg transition-colors shadow-sm ring-1 ring-inset ring-gray-200 dark:ring-slate-600 flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
          Print Summary
        </button>
        <button @click="resetForNextOrder" class="text-sm font-bold text-white bg-purple-600 hover:bg-purple-700 px-5 py-2.5 rounded-lg transition-all shadow-md hover:-translate-y-0.5 hover:shadow-lg flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7"/></svg>
          Scan Next Order
        </button>
      </div>
    </div>

    <!-- Session Summary -->
    <div class="flex flex-col md:flex-row gap-6 mb-6 mt-4">
      <div class="flex-1 bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border-2 border-dashed border-gray-200 dark:border-slate-700 flex items-center justify-between">
        <div>
          <p class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">Completed Orders</p>
          <h3 class="text-3xl font-black text-gray-800 dark:text-white">{{ completedCount }}</h3>
        </div>
        <div class="w-12 h-12 rounded-full bg-purple-50 dark:bg-slate-700 flex items-center justify-center text-purple-500">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
        </div>
      </div>
      <div class="flex-1 bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border-2 border-dashed border-gray-200 dark:border-slate-700 flex items-center justify-between">
        <div>
          <p class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">Total Items Picked</p>
          <h3 class="text-3xl font-black text-gray-800 dark:text-white">{{ totalPickedCount }}</h3>
        </div>
        <div class="w-12 h-12 rounded-full bg-green-50 dark:bg-slate-700 flex items-center justify-center text-green-500">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/></svg>
        </div>
      </div>
    </div>

    <!-- Picking History (collapsible) -->
    <div v-if="pickingLog.length > 0" class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 mb-6 overflow-hidden">
      <button @click="showLog = !showLog" class="w-full p-4 flex justify-between items-center text-sm font-bold text-gray-600 dark:text-gray-300 uppercase tracking-wider hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors">
        <span class="flex items-center gap-2">
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          Picking History ({{ pickingLog.length }} scans)
        </span>
        <svg class="w-4 h-4 transition-transform" :class="showLog ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
      </button>
      <div v-if="showLog" class="border-t border-gray-100 dark:border-slate-700 max-h-[300px] overflow-y-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 dark:bg-slate-700 sticky top-0">
            <tr>
              <th class="text-left px-4 py-2 text-xs font-bold text-gray-500 uppercase">#</th>
              <th class="text-left px-4 py-2 text-xs font-bold text-gray-500 uppercase">Time</th>
              <th class="text-left px-4 py-2 text-xs font-bold text-gray-500 uppercase">Item</th>
              <th class="text-left px-4 py-2 text-xs font-bold text-gray-500 uppercase">Barcode</th>
              <th class="text-right px-4 py-2 text-xs font-bold text-gray-500 uppercase">Qty</th>
              <th class="text-left px-4 py-2 text-xs font-bold text-gray-500 uppercase">UOM Factor</th>
              <th class="text-right px-4 py-2 text-xs font-bold text-gray-500 uppercase">Multiplier</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(log, idx) in pickingLog" :key="idx" class="border-t border-gray-50 dark:border-slate-600 hover:bg-gray-50 dark:hover:bg-slate-700/50">
              <td class="px-4 py-2 text-gray-400">{{ idx + 1 }}</td>
              <td class="px-4 py-2 text-gray-500 font-mono text-xs">{{ log.time }}</td>
              <td class="px-4 py-2 font-bold text-gray-700 dark:text-slate-200">{{ log.item_code }}</td>
              <td class="px-4 py-2 text-gray-500 font-mono text-xs">{{ log.barcode }}</td>
              <td class="px-4 py-2 text-right font-black text-green-700">{{ log.qty }}</td>
              <td class="px-4 py-2 text-gray-500">{{ log.uom_factor }}</td>
              <td class="px-4 py-2 text-right text-purple-600 font-bold">×{{ log.multiplier }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';

const emit = defineEmits(['alert']);
const props = defineProps({ isLoading: Boolean });

// State
const currentSO = ref(null);
const customerName = ref('');
const soStatus = ref(null);
const itemsToPick = ref([]);
const pickedItems = ref([]);
const barcodeMap = ref({});
const soScan = ref('');
const itemScan = ref('');
const flashSuccess = ref(false);
const lastScanInfo = ref('');
const manualQtyMultiplier = ref(1);
const pickingLog = ref([]);
const showLog = ref(false);

// Workflow state
const currentStep = ref(1); // 1=pick, 2=MR draft, 3=SE
const mrName = ref(null);
const sourceWarehouse = ref('');
const targetWarehouse = ref('');
const requiredByDate = ref('');
const costCenter = ref('');
const purposeOfTransfer = ref('');
const warehouses = ref([]);
const costCenters = ref([]);
const completedSE = ref({ so_name: '', customer_name: '', mr_name: '', se_name: '', items: [] });

const completedCount = ref(0);
const totalPickedCount = ref(0);
const isLoading = ref(false);

const soInputRef = ref(null);
const itemInputRef = ref(null);

// CSRF
const csrf_token = window?.frappe?.csrf_token || '';

const apiCall = async (method, args = {}) => {
  isLoading.value = true;
  try {
    const response = await fetch(`/api/method/${method}`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Frappe-CSRF-Token": csrf_token },
      body: JSON.stringify(args)
    });
    if (!response.ok) {
      let errMessage = `HTTP Error ${response.status}`;
      try {
        const data = await response.json();
        if (data.exc_type) errMessage = data.exc_type;
        if (data._server_messages) {
          const msgs = JSON.parse(data._server_messages);
          errMessage = JSON.parse(msgs[0]).message || errMessage;
        }
      } catch(e) {}
      throw new Error(errMessage);
    }
    const data = await response.json();
    if (data.message && data.message.error) throw new Error(data.message.error);
    return data.message;
  } catch (error) {
    emit('alert', error.message, 'error');
    throw error;
  } finally {
    isLoading.value = false;
  }
};

const percentage = computed(() => {
  const totalRemaining = itemsToPick.value.reduce((a, o) => a + o.qty, 0);
  const totalPicked = pickedItems.value.reduce((a, o) => a + o.qty, 0);
  const total = totalRemaining + totalPicked;
  if (total === 0) return 0;
  // Only show 100% when truly complete — prevents premature scanner disable
  if (totalRemaining === 0) return 100;
  return Math.min(99, Math.floor((totalPicked / total) * 100));
});

const stepClass = (step) => {
  if (step < currentStep.value) return 'text-green-600 bg-green-50';
  if (step === currentStep.value) return 'text-purple-700 bg-purple-50 ring-1 ring-purple-200';
  return 'text-gray-400 bg-gray-50';
};
const stepNumClass = (step) => {
  if (step < currentStep.value) return 'bg-green-500 text-white border-green-500';
  if (step === currentStep.value) return 'bg-purple-500 text-white border-purple-500';
  return 'bg-gray-200 text-gray-500 border-gray-300';
};

// Load warehouses/cost centers
onMounted(async () => {
  try {
    const data = await apiCall('order_picking.api.api.get_warehouses_and_cost_centers');
    warehouses.value = data.warehouses || [];
    costCenters.value = data.cost_centers || [];
  } catch(e) {}
  const today = new Date();
  // Use local date to avoid timezone mismatch with server transaction date
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  requiredByDate.value = `${yyyy}-${mm}-${dd}`;
  await nextTick();
  soInputRef.value?.focus();
});

const handleSOScan = async () => {
  const val = soScan.value.trim();
  if (!val) return;
  try {
    const data = await apiCall('order_picking.api.api.get_sales_order_items', { scan_input: val });
    if (data) {
      currentSO.value = data.so_name;
      customerName.value = data.customer_name || '';
      soStatus.value = data.status || null;
      itemsToPick.value = JSON.parse(JSON.stringify(data.items));
      pickedItems.value = [];
      barcodeMap.value = data.barcode_map || {};
      currentStep.value = 1;
      mrName.value = null;
      lastScanInfo.value = '';
      soScan.value = '';
      emit('alert', `Loaded Sales Order ${currentSO.value} — Customer: ${customerName.value}`, 'success');
      await nextTick();
      itemInputRef.value?.focus();
    }
  } catch(e) {
    soScan.value = '';
    soInputRef.value?.focus();
  }
};

const handleItemScan = () => {
  const val = itemScan.value.trim();
  if (!val) return;

  const multiplier = Math.max(1, Math.floor(manualQtyMultiplier.value || 1));

  // Check barcode map first
  const bcEntry = barcodeMap.value[val];
  let matchItemCode = null;
  let uomFactor = 1;

  if (bcEntry) {
    matchItemCode = bcEntry.item_code;
    uomFactor = bcEntry.qty || 1;
  } else {
    // Fallback: match by item_code directly
    const found = itemsToPick.value.find(i => i.item_code === val);
    if (found) matchItemCode = found.item_code;
  }

  if (!matchItemCode) {
    emit('alert', 'Barcode not found in this Sales Order!', 'error');
    itemScan.value = '';
    return;
  }

  const foundIndex = itemsToPick.value.findIndex(i => i.item_code === matchItemCode);
  if (foundIndex === -1 || itemsToPick.value[foundIndex].qty <= 0) {
    emit('alert', 'Item already fully picked!', 'error');
    itemScan.value = '';
    return;
  }

  // Total qty = UOM factor × manual multiplier, capped at remaining
  const scanQty = uomFactor * multiplier;
  const remaining = itemsToPick.value[foundIndex].qty;
  const actualQty = Math.min(scanQty, remaining);

  itemsToPick.value[foundIndex].qty -= actualQty;

  const pickedIndex = pickedItems.value.findIndex(i => i.item_code === matchItemCode);
  if (pickedIndex !== -1) {
    pickedItems.value[pickedIndex].qty += actualQty;
  } else {
    pickedItems.value.push({
      item_code: matchItemCode,
      item_name: itemsToPick.value[foundIndex].item_name,
      image: itemsToPick.value[foundIndex].image,
      uom: itemsToPick.value[foundIndex].uom,
      qty: actualQty
    });
  }

  // Log this scan
  const now = new Date();
  pickingLog.value.push({
    time: now.toLocaleTimeString(),
    item_code: matchItemCode,
    barcode: val,
    qty: actualQty,
    uom_factor: uomFactor > 1 ? `${uomFactor}/scan` : '1 (unit)',
    multiplier: multiplier
  });

  lastScanInfo.value = `Scanned ${matchItemCode} × ${actualQty}`
    + (uomFactor > 1 ? ` (UOM: ${uomFactor} × ${multiplier})` : (multiplier > 1 ? ` (× ${multiplier})` : ''))
    + (actualQty < scanQty ? ` — capped at remaining` : '');

  flashSuccess.value = true;
  setTimeout(() => flashSuccess.value = false, 200);

  // Reset multiplier back to 1 after scan
  manualQtyMultiplier.value = 1;

  if (percentage.value === 100) {
    emit('alert', 'All items picked! Fill warehouse details and create Material Request.', 'success');
  }

  itemScan.value = '';
};

const printPickList = () => {
  const rows = pickedItems.value.map((item, idx) =>
    `<tr><td style="padding:6px 12px;border:1px solid #ddd">${idx+1}</td><td style="padding:6px 12px;border:1px solid #ddd;font-weight:bold">${item.item_code}</td><td style="padding:6px 12px;border:1px solid #ddd">${item.item_name||''}</td><td style="padding:6px 12px;border:1px solid #ddd;text-align:right;font-weight:bold">${item.qty}</td><td style="padding:6px 12px;border:1px solid #ddd">${item.uom||'Nos'}</td></tr>`
  ).join('');
  const logRows = pickingLog.value.map((log, idx) =>
    `<tr><td style="padding:4px 8px;border:1px solid #eee;font-size:11px">${idx+1}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px">${log.time}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px;font-weight:bold">${log.item_code}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px;font-family:monospace">${log.barcode}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px;text-align:right;font-weight:bold">${log.qty}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px">×${log.multiplier} (${log.uom_factor})</td></tr>`
  ).join('');
  const html = `<html><head><title>B2B Pick List — ${currentSO.value}</title><style>body{font-family:system-ui,sans-serif;padding:30px;color:#333}table{border-collapse:collapse;width:100%}th{background:#f3f4f6;text-align:left;padding:8px 12px;border:1px solid #ddd;font-size:12px;text-transform:uppercase}</style></head><body>` +
    `<h1 style="margin:0 0 4px">B2B Pick List</h1>` +
    `<p style="color:#666;margin:0 0 4px"><strong>Sales Order:</strong> ${currentSO.value} &nbsp; <strong>Customer:</strong> ${customerName.value} &nbsp; <strong>Status:</strong> ${soStatus.value||'N/A'}</p>` +
    `<p style="color:#999;margin:0 0 20px;font-size:12px">Printed: ${new Date().toLocaleString()}</p>` +
    `<h3 style="margin:0 0 8px">Picked Items Summary</h3>` +
    `<table><thead><tr><th>#</th><th>Item Code</th><th>Item Name</th><th style="text-align:right">Qty</th><th>UOM</th></tr></thead><tbody>${rows}</tbody></table>` +
    (logRows ? `<h3 style="margin:24px 0 8px">Scan Log</h3><table><thead><tr><th>#</th><th>Time</th><th>Item</th><th>Barcode</th><th style="text-align:right">Qty</th><th>Details</th></tr></thead><tbody>${logRows}</tbody></table>` : '') +
    `</body></html>`;
  const w = window.open('', '_blank');
  w.document.write(html);
  w.document.close();
  w.focus();
  w.print();
};

const createMR = async () => {
  try {
    const items = pickedItems.value.map(i => ({ item_code: i.item_code, qty: i.qty, uom: i.uom || 'Nos' }));
    const data = await apiCall('order_picking.api.api.create_b2b_material_request', {
      so_name: currentSO.value,
      items: JSON.stringify(items),
      source_warehouse: sourceWarehouse.value,
      target_warehouse: targetWarehouse.value,
      required_by_date: requiredByDate.value
    });
    mrName.value = data.mr_name;
    currentStep.value = 2;
    emit('alert', `Material Request ${data.mr_name} created successfully!`, 'success');
  } catch(e) {}
};

const submitMR = async () => {
  try {
    await apiCall('order_picking.api.api.submit_b2b_material_request', { mr_name: mrName.value });
    currentStep.value = 3;
    purposeOfTransfer.value = `Transfer by B2B Order Pick for ${customerName.value}`;
    emit('alert', `Material Request ${mrName.value} submitted!`, 'success');
  } catch(e) {}
};

const createSE = async () => {
  try {
    const data = await apiCall('order_picking.api.api.create_b2b_stock_entry', {
      mr_name: mrName.value,
      cost_center: costCenter.value,
      purpose_of_transfer: purposeOfTransfer.value
    });
    emit('alert', `Stock Entry ${data.se_name} created & submitted!`, 'success');
    completedCount.value++;
    totalPickedCount.value += pickedItems.value.reduce((a, o) => a + o.qty, 0);

    // Store completion data for summary / print
    completedSE.value = {
      so_name: data.so_name || currentSO.value || '',
      customer_name: data.customer_name || customerName.value || '',
      mr_name: data.mr_name || mrName.value || '',
      se_name: data.se_name || '',
      items: data.items || pickedItems.value.map(i => ({
        item_code: i.item_code,
        item_name: i.item_name,
        qty: i.qty,
        uom: i.uom || 'Nos',
        from_warehouse: sourceWarehouse.value,
        to_warehouse: targetWarehouse.value
      }))
    };

    // Go to step 4 (completed) instead of immediately resetting
    currentStep.value = 4;
  } catch(e) {}
};

const printCompletedSummary = () => {
  const c = completedSE.value;
  const rows = c.items.map((item, idx) =>
    `<tr><td style="padding:6px 12px;border:1px solid #ddd">${idx+1}</td><td style="padding:6px 12px;border:1px solid #ddd;font-weight:bold">${item.item_code}</td><td style="padding:6px 12px;border:1px solid #ddd">${item.item_name||''}</td><td style="padding:6px 12px;border:1px solid #ddd;text-align:right;font-weight:bold">${item.qty}</td><td style="padding:6px 12px;border:1px solid #ddd">${item.uom||'Nos'}</td><td style="padding:6px 12px;border:1px solid #ddd;font-size:11px">${item.from_warehouse||''}</td><td style="padding:6px 12px;border:1px solid #ddd;font-size:11px">${item.to_warehouse||''}</td></tr>`
  ).join('');
  const logRows = pickingLog.value.map((log, idx) =>
    `<tr><td style="padding:4px 8px;border:1px solid #eee;font-size:11px">${idx+1}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px">${log.time}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px;font-weight:bold">${log.item_code}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px;font-family:monospace">${log.barcode}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px;text-align:right;font-weight:bold">${log.qty}</td><td style="padding:4px 8px;border:1px solid #eee;font-size:11px">&times;${log.multiplier} (${log.uom_factor})</td></tr>`
  ).join('');
  const html = `<html><head><title>B2B Pick Summary &mdash; ${c.so_name}</title><style>body{font-family:system-ui,sans-serif;padding:30px;color:#333}table{border-collapse:collapse;width:100%}th{background:#f3f4f6;text-align:left;padding:8px 12px;border:1px solid #ddd;font-size:12px;text-transform:uppercase}.badge{display:inline-block;padding:4px 10px;border-radius:6px;font-size:12px;font-weight:bold;margin-right:8px}</style></head><body>` +
    `<h1 style="margin:0 0 4px">B2B Order Pick &mdash; Completion Summary</h1>` +
    `<p style="color:#666;margin:0 0 4px"><strong>Sales Order:</strong> ${c.so_name} &nbsp; <strong>Customer:</strong> ${c.customer_name}</p>` +
    `<p style="color:#666;margin:0 0 4px"><span class="badge" style="background:#fef3c7;color:#92400e">MR: ${c.mr_name}</span><span class="badge" style="background:#d1fae5;color:#065f46">SE: ${c.se_name}</span></p>` +
    `<p style="color:#999;margin:0 0 20px;font-size:12px">Printed: ${new Date().toLocaleString()}</p>` +
    `<h3 style="margin:0 0 8px">Transfer Items</h3>` +
    `<table><thead><tr><th>#</th><th>Item Code</th><th>Item Name</th><th style="text-align:right">Qty</th><th>UOM</th><th>Source WH</th><th>Dest WH</th></tr></thead><tbody>${rows}</tbody></table>` +
    (logRows ? `<h3 style="margin:24px 0 8px">Scan Log (${pickingLog.value.length} scans)</h3><table><thead><tr><th>#</th><th>Time</th><th>Item</th><th>Barcode</th><th style="text-align:right">Qty</th><th>Details</th></tr></thead><tbody>${logRows}</tbody></table>` : '') +
    `</body></html>`;
  const w = window.open('', '_blank');
  w.document.write(html);
  w.document.close();
  w.focus();
  w.print();
};

const resetForNextOrder = async () => {
  currentSO.value = null;
  customerName.value = '';
  soStatus.value = null;
  itemsToPick.value = [];
  pickedItems.value = [];
  barcodeMap.value = {};
  mrName.value = null;
  currentStep.value = 1;
  sourceWarehouse.value = '';
  targetWarehouse.value = '';
  costCenter.value = '';
  purposeOfTransfer.value = '';
  lastScanInfo.value = '';
  manualQtyMultiplier.value = 1;
  pickingLog.value = [];
  showLog.value = false;
  completedSE.value = { so_name: '', customer_name: '', mr_name: '', se_name: '', items: [] };
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  requiredByDate.value = `${yyyy}-${mm}-${dd}`;
  await nextTick();
  soInputRef.value?.focus();
};

// Expose refs for parent focus management
defineExpose({ soInputRef, itemInputRef });
</script>
