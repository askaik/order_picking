<template>
  <div class="picking-wrapper max-w-5xl mx-auto p-5">
    <!-- Header / Branding -->
    <div class="mb-6 flex justify-between items-center bg-white dark:bg-slate-800 p-4 shadow-sm rounded-lg border border-gray-100 dark:border-slate-700">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-green-50 text-green-600 rounded-lg flex items-center justify-center font-bold text-xl ring-1 ring-green-100 shadow-sm">
          OP
        </div>
        <div>
          <h1 class="text-xl font-bold text-gray-800 dark:text-slate-100">Order Picking</h1>
          <p class="text-xs text-gray-500 dark:text-gray-400 font-medium tracking-wide flex items-center gap-1">
            <span v-if="orderPickId">Session: 
                <a :href="'/app/order-pick/' + orderPickId" target="_blank" class="text-blue-600 dark:text-blue-400 font-bold bg-blue-50 dark:bg-blue-900/40 px-1.5 py-0.5 rounded hover:underline hover:bg-blue-100 dark:hover:bg-blue-800 transition-colors">
                    {{ orderPickId }}
                </a>
            </span>
            <span v-else class="text-gray-400 dark:text-gray-500">Loading Session...</span>
          </p>
        </div>
      </div>
      <div>
         <button @click="backToErp" class="text-sm font-semibold text-gray-600 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-md transition-colors shadow-sm ring-1 ring-inset ring-gray-200 flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Exit Scanner
        </button>
      </div>
    </div>

    <!-- Error/Alert Bar (Global) -->
    <Transition name="fade">
      <div v-if="alertMessage" :class="alertClasses" class="mb-4 p-4 rounded-lg shadow-sm font-medium flex justify-between items-center transition-all duration-300">
        <span class="flex items-center gap-2">
          <svg v-if="alertType === 'error'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          {{ alertMessage }}
        </span>
        <button @click="alertMessage = ''" class="text-gray-500 hover:text-gray-700 font-bold p-1 rounded hover:bg-black/5 transition-colors">&times;</button>
      </div>
    </Transition>

    <!-- Progress Bar Section -->
    <div class="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 mb-6 relative overflow-hidden">
      <!-- Decorator element -->
      <div class="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-blue-400 to-indigo-500"></div>
      
      <div class="flex justify-between items-end mb-3">
        <h4 class="text-sm font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
           <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
           Picking Progress
        </h4>
        <div class="text-2xl font-black" :class="percentage === 100 ? 'text-green-600' : 'text-blue-600'">
            {{ percentage }}%
        </div>
      </div>
      
      <div class="w-full bg-gray-100 rounded-full h-4 mb-2 overflow-hidden shadow-inner ring-1 ring-inset ring-gray-200/50">
        <div 
          class="h-4 rounded-full transition-all duration-500 ease-out shadow-[0_0_10px_rgba(0,0,0,0.1)] relative" 
          :class="progressColorClass"
          :style="{ width: percentage + '%' }"
        >
          <!-- Shimmer effect -->
          <div class="absolute inset-0 bg-white/20 w-full animate-[shimmer_2s_infinite] -skew-x-12 translate-x-[-100%]"></div>
        </div>
      </div>
      
      <div class="flex justify-between items-center mt-4 h-12">
        <div class="text-sm font-medium text-gray-500 bg-gray-50 dark:bg-slate-700 dark:text-slate-200 px-3 py-1.5 rounded-md border border-gray-100 dark:border-slate-600 shadow-sm" v-if="currentInvoice">
            Active: <span class="font-bold text-gray-800 dark:text-white">{{ currentInvoice }}</span>
        </div>
        <div v-else></div>

         <!-- Action Buttons -->
        <div class="flex gap-3">
            <button 
                v-if="percentage === 100 && currentInvoice" 
                @click="markReady" 
                class="bg-green-600 hover:bg-green-700 active:bg-green-800 text-white font-bold py-2.5 px-6 rounded-lg text-sm shadow-md transition-all hover:-translate-y-0.5 hover:shadow-lg flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              Mark Ready & Next
            </button>

            <button 
                v-if="orderPickId && (!currentInvoice || percentage === 100)" 
                @click="submitOrderPick" 
                class="bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white font-bold py-2.5 px-6 rounded-lg text-sm shadow-md transition-all hover:-translate-y-0.5 hover:shadow-lg flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
              Submit Dispatch Report
            </button>
        </div>
      </div>
    </div>

    <!-- Scan Inputs Section -->
    <div class="flex flex-col md:flex-row gap-4 mb-6">
      <div class="flex-1 relative group">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
           <svg class="w-6 h-6 text-gray-400 group-focus-within:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"></path></svg>
        </div>
        <input 
          v-model="invoiceScan" 
          @keyup.enter="handleInvoiceScan"
          type="text" 
          id="scan_invoice_input" 
          class="w-full pl-12 pr-4 py-4 text-lg border-2 border-gray-200 dark:border-slate-600 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all shadow-sm font-medium bg-white dark:bg-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500" 
          placeholder="Scan Invoice Barcode..." 
          :disabled="isLoading"
          ref="invoiceInputRef"
        >
      </div>

      <div class="flex-1 relative group">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
           <svg class="w-6 h-6 text-gray-400 group-focus-within:text-indigo-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm14 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"></path></svg>
        </div>
        <input 
          v-model="itemScan" 
          @keyup.enter="handleItemScan"
          type="text" 
          id="scan_item_input" 
          :class="{'ring-4 ring-green-400/50 bg-green-50': flashSuccess, 'border-gray-200 focus:border-indigo-500 focus:ring-indigo-500/20': !flashSuccess}"
          class="w-full pl-12 pr-4 py-4 text-lg border-2 rounded-xl focus:ring-4 transition-all shadow-sm font-medium bg-white dark:bg-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 disabled:bg-gray-100 dark:disabled:bg-slate-900 disabled:cursor-not-allowed disabled:border-gray-200 dark:disabled:border-slate-700" 
          placeholder="Scan Item Barcode..." 
          :disabled="!currentInvoice || percentage === 100 || isLoading"
          ref="itemInputRef"
        >
      </div>
    </div>

    <!-- Lists Section -->
    <div class="flex flex-col md:flex-row gap-6">
      
      <!-- Items to Pick -->
      <div class="flex-1 bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 flex flex-col min-h-[400px]">
        <h4 class="text-sm font-bold text-gray-700 uppercase tracking-wider mb-4 border-b pb-3 flex justify-between items-center">
          <span class="flex items-center gap-2">
             <div class="w-2 h-2 rounded-full bg-blue-500"></div> Items to Pick
          </span>
          <span class="bg-gray-100 text-gray-600 px-2 py-0.5 rounded text-xs">{{ itemsToPick.filter(i => i.qty > 0).length }} pending</span>
        </h4>
        
        <div class="flex-1 overflow-y-auto pr-2 -mr-2 space-y-2 relative" v-if="itemsToPick.length > 0">
          <div 
            v-for="item in itemsToPick.filter(i => i.qty > 0)" 
            :key="item.item_code" 
            class="flex justify-between items-center bg-gray-50 dark:bg-slate-700 border border-gray-100 dark:border-slate-600 p-3 rounded-lg hover:border-blue-200 hover:shadow-sm transition-all group"
          >
            <div class="font-semibold text-gray-800 dark:text-slate-100 tracking-wide">{{ item.item_code }}</div>
            <div class="text-lg font-black bg-white dark:bg-slate-800 px-3 py-1 rounded shadow-sm border border-gray-200 dark:border-slate-500 group-hover:border-blue-300 group-hover:text-blue-700 dark:group-hover:text-blue-400 transition-colors">{{ item.qty }}</div>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col items-center justify-center text-gray-400 h-full opacity-60">
            <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
            <p class="font-medium text-lg">Scan an invoice to begin.</p>
        </div>
      </div>

      <!-- Picked Items -->
      <div class="flex-1 bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 flex flex-col min-h-[400px]">
        <h4 class="text-sm font-bold text-gray-700 uppercase tracking-wider mb-4 border-b pb-3 flex justify-between items-center">
            <span class="flex items-center gap-2">
                 <div class="w-2 h-2 rounded-full bg-green-500"></div> Picked Items
            </span>
            <span class="bg-green-50 text-green-700 px-2 py-0.5 rounded text-xs border border-green-100">{{ pickedItems.reduce((acc, obj) => acc + obj.qty, 0) }} total</span>
        </h4>
        
        <div class="flex-1 overflow-y-auto pr-2 -mr-2 space-y-2 relative" v-if="pickedItems.length > 0">
          <div 
            v-for="item in pickedItems" 
            :key="item.item_code" 
            class="flex justify-between items-center bg-green-50 border border-green-100 p-3 rounded-lg shadow-sm"
          >
             <div class="font-semibold text-green-800 dark:text-green-300 tracking-wide flex items-center gap-2">
                <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ item.item_code }}
            </div>
            <div class="text-lg font-black bg-white dark:bg-slate-800 text-green-700 dark:text-green-400 px-3 py-1 rounded shadow-sm border border-green-200 dark:border-green-800">{{ item.qty }}</div>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col items-center justify-center text-gray-400 h-full opacity-60">
             <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
            <p class="font-medium">No items picked yet.</p>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';

// State
const orderPickId = ref(null);
const currentInvoice = ref(null);
const itemsToPick = ref([]);
const pickedItems = ref([]);
const invoiceScan = ref('');
const itemScan = ref('');
const isLoading = ref(false);
const flashSuccess = ref(false);

const invoiceInputRef = ref(null);
const itemInputRef = ref(null);

// Alert State
const alertMessage = ref('');
const alertType = ref('success');

// Helpers for the Frappe Fetch API
const csrf_token = window?.frappe?.csrf_token || '';

const apiCall = async (method, args = {}) => {
  isLoading.value = true;
  try {
    const response = await fetch(`/api/method/${method}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Frappe-CSRF-Token": csrf_token
      },
      body: JSON.stringify(args)
    });
    
    // Check http status
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
    
    // Check python generic exception block
    if (data.message && data.message.error) {
        throw new Error(data.message.error);
    }
    
    return data.message;
  } catch (error) {
    showAlert(error.message, 'error');
    alert(`Backend Error: ${error.message}`);
    throw error;
  } finally {
    isLoading.value = false;
  }
};

const showAlert = (message, type = 'success') => {
  alertMessage.value = message;
  alertType.value = type;
  if(type === 'success') {
      setTimeout(() => alertMessage.value = '', 4000);
  }
};

const alertClasses = computed(() => {
  return alertType.value === 'error' 
    ? 'bg-red-50 text-red-700 border border-red-200' 
    : 'bg-green-50 text-green-700 border border-green-200';
});

// Calculate Percentage
const percentage = computed(() => {
  const totalRemaining = itemsToPick.value.reduce((acc, obj) => acc + obj.qty, 0);
  const totalPicked = pickedItems.value.reduce((acc, obj) => acc + obj.qty, 0);
  const total = totalRemaining + totalPicked;
  
  if (total === 0) return 0;
  return Math.round((totalPicked / total) * 100);
});

// Color Class
const progressColorClass = computed(() => {
  if (percentage.value === 100) return 'bg-gradient-to-r from-green-400 to-green-500';
  return 'bg-gradient-to-r from-blue-400 to-indigo-500';
});

// On Mount
onMounted(async () => {
    try {
        const id = await apiCall('order_picking.api.api.get_active_order_pick');
        orderPickId.value = id;
    } catch (e) {
        console.error("Failed to fetch session", e);
    }
    invoiceInputRef.value?.focus();
});

// Handlers
const handleInvoiceScan = async () => {
  const val = invoiceScan.value.trim();
  if (!val) return;
  
  try {
    const data = await apiCall('order_picking.api.api.get_invoice_items', { scan_input: val });
    if(data) {
        currentInvoice.value = data.invoice_name;
        // Deep copy
        itemsToPick.value = JSON.parse(JSON.stringify(data.items));
        pickedItems.value = [];
        invoiceScan.value = '';
        showAlert(`Loaded invoice ${currentInvoice.value}`);
        
        await nextTick();
        itemInputRef.value?.focus();
    }
  } catch (e) {
      invoiceScan.value = '';
      invoiceInputRef.value?.focus();
  }
};

const handleItemScan = () => {
  const val = itemScan.value.trim();
  if (!val) return;
  
  const foundIndex = itemsToPick.value.findIndex(i => i.item_code === val || i.barcode === val);
  
  if (foundIndex !== -1 && itemsToPick.value[foundIndex].qty > 0) {
      itemsToPick.value[foundIndex].qty--;
      
      const pickedIndex = pickedItems.value.findIndex(i => i.item_code === itemsToPick.value[foundIndex].item_code);
      if(pickedIndex !== -1) {
          pickedItems.value[pickedIndex].qty++;
      } else {
          pickedItems.value.push({
              item_code: itemsToPick.value[foundIndex].item_code,
              qty: 1
          });
      }
      
      flashSuccess.value = true;
      setTimeout(() => flashSuccess.value = false, 200);
      
      if(percentage.value === 100) {
         showAlert('Invoice Fully Picked! Ready to mark.', 'success');
      }
  } else {
      showAlert('Item not found in invoice or already fully picked!', 'error');
  }
  
  itemScan.value = '';
};

const markReady = async () => {
    if(!currentInvoice.value) return;
    try {
        await apiCall('order_picking.api.api.mark_invoice_as_ready', { 
            invoice_name: currentInvoice.value, 
            order_pick_id: orderPickId.value 
        });
        showAlert('Invoice attached to Order Pick & Marked Ready!');
        currentInvoice.value = null;
        itemsToPick.value = [];
        pickedItems.value = [];
        await nextTick();
        invoiceInputRef.value?.focus();
    } catch(e) {}
};

const submitOrderPick = async () => {
    if(!orderPickId.value) return;
    if(confirm("Submit this Order Pick? This will create a Dispatch Order.")) {
        try {
            await apiCall('order_picking.api.api.submit_order_pick', {
                order_pick_id: orderPickId.value
            });
            showAlert('Order Pick Submitted successfully! A new Dispatch Order has been created.', 'success');
            
            // Clear current states 
            orderPickId.value = null;
            currentInvoice.value = null;
            itemsToPick.value = [];
            pickedItems.value = [];
            invoiceScan.value = '';
            itemScan.value = '';
            
            // Wait 300ms for UI to clear, then ask user
            setTimeout(async () => {
                alertMessage.value = ''; // clear success message early so it doesn't block
                if(confirm("Session cleared successfully.\n\nDo you want to create a new session with a new Session ID?\n(Click Cancel to exit to ERPNext)")) {
                    try {
                        const id = await apiCall('order_picking.api.api.get_active_order_pick', { force_new: 1 });
                        orderPickId.value = id;
                        await nextTick();
                        invoiceInputRef.value?.focus();
                    } catch(e) {}
                } else {
                    backToErp();
                }
            }, 300);
            
        } catch(e) {
            // Error is already handled by apiCall Native Alert
        }
    }
};

const backToErp = () => {
    window.location.href = '/app/workspace/Order%20Picking';
};

</script>

<style>
@keyframes shimmer {
  100% {
    transform: translateX(100%) skewX(-12deg);
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
