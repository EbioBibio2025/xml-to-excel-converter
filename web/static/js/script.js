/**
 * XML to Excel Converter - نسخه وب
 */

let uploadedFile = null;
let fileInfo = null;
let isConverting = false;
let isUploading = false;

const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const fileInfoDiv = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const settingsSection = document.getElementById('settingsSection');
const infoSection = document.getElementById('infoSection');
const infoGrid = document.getElementById('infoGrid');
const resultsSection = document.getElementById('resultsSection');
const resultsStats = document.getElementById('resultsStats');
const downloadList = document.getElementById('downloadList');
const logContent = document.getElementById('logContent');
const convertBtn = document.getElementById('convertBtn');
const overlay = document.getElementById('overlay');
const overlayText = document.getElementById('overlayText');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const uploadProgress = document.getElementById('uploadProgress');
const recordCount = document.getElementById('recordCount');

// ==================== Drag and Drop ====================
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// ==================== مدیریت فایل ====================
function handleFile(file) {
    if (!file.name.toLowerCase().endsWith('.xml')) {
        addLog('فایل باید با پسوند XML باشد', 'error');
        return;
    }
    
    if (file.size > 50 * 1024 * 1024) {
        addLog('حجم فایل نباید بیشتر از ۵۰ مگابایت باشد', 'error');
        return;
    }
    
    uploadedFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatSize(file.size);
    fileInfoDiv.style.display = 'flex';
    uploadBox.style.display = 'none';
    
    addLog(`فایل انتخاب شد: ${file.name} (${formatSize(file.size)})`, 'info');
    uploadFile(file);
}

function removeFile() {
    uploadedFile = null;
    fileInfo = null;
    fileInfoDiv.style.display = 'none';
    uploadBox.style.display = 'block';
    settingsSection.style.display = 'none';
    infoSection.style.display = 'none';
    resultsSection.style.display = 'none';
    fileInput.value = '';
    convertBtn.disabled = true;
    addLog('فایل حذف شد', 'info');
}

function formatSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;
    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }
    return `${size.toFixed(2)} ${units[unitIndex]}`;
}

// ==================== آپلود ====================
async function uploadFile(file) {
    if (isUploading) return;
    isUploading = true;
    
    const formData = new FormData();
    formData.append('file', file);
    
    uploadProgress.style.display = 'block';
    progressFill.style.width = '0%';
    progressText.textContent = 'در حال آپلود...';
    
    try {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            if (progress <= 90) {
                progressFill.style.width = progress + '%';
            }
        }, 100);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(interval);
        progressFill.style.width = '100%';
        
        const result = await response.json();
        
        if (result.success) {
            fileInfo = result.file_info;
            progressText.textContent = '✅ آپلود کامل شد!';
            addLog('فایل با موفقیت آپلود شد', 'success');
            showFileInfo(fileInfo);
            settingsSection.style.display = 'block';
            convertBtn.disabled = false;
            if (fileInfo.structure && fileInfo.structure.total_elements) {
                recordCount.textContent = `${fileInfo.structure.total_elements} المان`;
            }
        } else {
            progressText.textContent = '❌ خطا در آپلود';
            addLog(`خطا در آپلود: ${result.error}`, 'error');
        }
    } catch (error) {
        progressText.textContent = '❌ خطا در آپلود';
        addLog(`خطا: ${error.message}`, 'error');
    } finally {
        isUploading = false;
        setTimeout(() => {
            uploadProgress.style.display = 'none';
        }, 1500);
    }
}

// ==================== اطلاعات فایل ====================
function showFileInfo(info) {
    const structure = info.structure;
    infoGrid.innerHTML = `
        <div class="info-item">
            <span class="label">🏷️ تگ ریشه</span>
            <span class="value">${structure.root_tag || 'نامشخص'}</span>
        </div>
        <div class="info-item">
            <span class="label">📦 تعداد المان‌ها</span>
            <span class="value">${structure.total_elements || 0}</span>
        </div>
        <div class="info-item">
            <span class="label">📏 حداکثر عمق</span>
            <span class="value">${structure.max_depth || 0}</span>
        </div>
        <div class="info-item">
            <span class="label">🔖 تگ‌های منحصر‌به‌فرد</span>
            <span class="value">${structure.unique_tags ? structure.unique_tags.slice(0, 5).join(', ') : ''}${structure.unique_tags && structure.unique_tags.length > 5 ? '...' : ''}</span>
        </div>
    `;
    infoSection.style.display = 'block';
}

// ==================== تبدیل ====================
function startConversion() {
    convertFile();
}

async function convertFile() {
    if (isConverting) return;
    if (!fileInfo) {
        addLog('لطفاً ابتدا یک فایل آپلود کنید', 'warning');
        return;
    }
    
    isConverting = true;
    convertBtn.disabled = true;
    convertBtn.innerHTML = '<span style="display:inline-block;width:16px;height:16px;border:2px solid white;border-top-color:transparent;border-radius:50%;animation:spin 0.8s linear infinite;"></span> در حال تبدیل...';
    
    overlay.style.display = 'flex';
    overlayText.textContent = 'در حال پردازش فایل...';
    
    const targetTag = document.getElementById('targetTag').value.trim();
    const outputFormat = document.getElementById('outputFormat').value;
    const outputName = document.getElementById('outputName').value.trim() || 'converted';
    const generateSummary = document.getElementById('generateSummary').checked;
    
    addLog('شروع تبدیل فایل...', 'info');
    addLog(`فرمت خروجی: ${outputFormat}`, 'info');
    if (targetTag) addLog(`تگ هدف: ${targetTag}`, 'info');
    
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                filename: fileInfo.unique_filename,
                target_tag: targetTag,
                output_format: outputFormat,
                output_name: outputName,
                generate_summary: generateSummary
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            addLog('✅ تبدیل با موفقیت انجام شد!', 'success');
            showResults(result);
            overlayText.textContent = '✅ تبدیل کامل شد!';
            setTimeout(() => { overlay.style.display = 'none'; }, 1000);
        } else {
            addLog(`❌ خطا در تبدیل: ${result.error}`, 'error');
            overlay.style.display = 'none';
        }
    } catch (error) {
        addLog(`❌ خطا: ${error.message}`, 'error');
        overlay.style.display = 'none';
    } finally {
        isConverting = false;
        convertBtn.disabled = false;
        convertBtn.innerHTML = '<i class="fas fa-play"></i> شروع تبدیل';
    }
}

// ==================== نمایش نتایج ====================
function showResults(result) {
    const info = result.conversion_info;
    const files = result.files || [];
    
    resultsStats.innerHTML = `
        <div class="stat-card">
            <div class="number">${info.record_count || 0}</div>
            <div class="label">تعداد رکوردها</div>
        </div>
        <div class="stat-card">
            <div class="number">${info.headers ? info.headers.length : 0}</div>
            <div class="label">تعداد ستون‌ها</div>
        </div>
        <div class="stat-card">
            <div class="number">${files.length}</div>
            <div class="label">فایل‌های خروجی</div>
        </div>
    `;
    
    if (files.length > 0) {
        downloadList.innerHTML = files.map((file, index) => {
            const filePath = file.path.replace(/\\/g, '/');
            return `
                <div class="download-item" style="animation-delay: ${index * 0.1}s">
                    <div class="info">
                        <span class="name"><i class="fas fa-file"></i> ${file.name}</span>
                        <span class="size"><i class="fas fa-weight-hanging"></i> ${file.size}</span>
                    </div>
                    <a href="/api/download/${encodeURIComponent(filePath)}" 
                       class="btn btn-success btn-sm" download>
                        <i class="fas fa-download"></i> دانلود
                    </a>
                </div>
            `;
        }).join('');
    } else {
        downloadList.innerHTML = `<p style="color:#7f8c8d;text-align:center;padding:20px;">هیچ فایلی ایجاد نشد</p>`;
    }
    
    resultsSection.style.display = 'block';
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

// ==================== لاگ ====================
function addLog(message, type = 'info') {
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    const now = new Date();
    const time = now.toLocaleTimeString('fa-IR');
    const iconMap = {
        'info': 'fa-info-circle',
        'success': 'fa-check-circle',
        'warning': 'fa-exclamation-triangle',
        'error': 'fa-times-circle'
    };
    entry.innerHTML = `
        <i class="fas ${iconMap[type] || 'fa-info-circle'}"></i>
        <span>[${time}] ${message}</span>
    `;
    logContent.appendChild(entry);
    logContent.scrollTop = logContent.scrollHeight;
}

function clearLog() {
    logContent.innerHTML = '';
    addLog('لاگ پاک شد', 'info');
}

function clearAll() {
    removeFile();
    clearLog();
    resultsSection.style.display = 'none';
    settingsSection.style.display = 'none';
    infoSection.style.display = 'none';
    addLog('همه چیز پاک شد', 'info');
}

// ==================== راه‌اندازی ====================
addLog('✅ برنامه آماده است. فایل XML خود را آپلود کنید.', 'info');
convertBtn.disabled = true;