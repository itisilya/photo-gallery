<template>
  <div class="home">
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M23 19C23 19.5304 22.7893 20.0391 22.4142 20.4142C22.0391 20.7893 21.5304 21 21 21H3C2.46957 21 1.96086 20.7893 1.58579 20.4142C1.21071 20.0391 1 19.5304 1 19V8C1 7.46957 1.21071 6.96086 1.58579 6.58579C1.96086 6.21071 2.46957 6 3 6H7L9 3H15L17 6H21C21.5304 6 22.0391 6.21071 22.4142 6.58579C22.7893 6.96086 23 7.46957 23 8V19Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 17C14.2091 17 16 15.2091 16 13C16 10.7909 14.2091 9 12 9C9.79086 9 8 10.7909 8 13C8 15.2091 9.79086 17 12 17Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h1 class="hero-title">Фотогалерея</h1>
        <div class="hero-stats">
          <div class="stat">
            <div class="stat-number">{{ photos.length }}</div>
            <div class="stat-label">Фотографий</div>
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <!-- Форма загрузки -->
      <div class="upload-section">
        <div class="section-header">
          <div class="section-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M17 8L12 3L7 8" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 3V15" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="section-title">Загрузить новое фото</h2>
        </div>

        <div class="upload-card">
          <form @submit.prevent="handleSubmit" class="upload-form">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-text">Название *</span>
                  <span class="label-required">Обязательно</span>
                </label>
                <input
                  v-model="form.title"
                  placeholder="Введите название"
                  required
                  class="form-input"
                />
                <div class="input-hint">Например: "Закат на море" или "Горный пейзаж"</div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <span class="label-text">Описание</span>
                  <span class="label-optional">Необязательно</span>
                </label>
                <input
                  v-model="form.description"
                  placeholder="Введите описание фото"
                  class="form-input"
                />
                <div class="input-hint">Максимум 200 символов</div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-text">Выберите изображение</span>
                <span class="label-required">Обязательно</span>
              </label>
              <div
                class="file-upload-area"
                :class="{ 'has-file': file }"
                @dragover.prevent
                @drop="handleFileDrop"
              >
                <div class="upload-icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M14 2H6C4.9 2 4.01 2.9 4.01 4L4 20C4 21.1 4.89 22 5.99 22H18C19.1 22 20 21.1 20 20V8L14 2Z" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M14 2V8H20" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M16 13H13V16H11V13H8V11H11V8H13V11H16V13Z" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="upload-text">
                  <span v-if="file" class="file-name">{{ file.name }}</span>
                  <span v-else>
                    Перетащите файл сюда или
                    <label for="file-input" class="browse-link">выберите на компьютере</label>
                  </span>
                </div>
                <div class="upload-hint">JPEG, PNG • Максимум 5 МБ</div>
                <input
                  id="file-input"
                  type="file"
                  @change="onFileChange"
                  accept="image/jpeg,image/png"
                  class="file-input"
                />
              </div>
            </div>

            <div class="form-actions">
              <button
                type="submit"
                :disabled="uploadLoading || !file || !form.title"
                class="upload-button"
                :class="{ 'loading': uploadLoading }"
              >
                <span class="button-content">
                  <span v-if="uploadLoading" class="spinner"></span>
                  <span v-else>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M17 8L12 3L7 8" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M12 3V15" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </span>
                  {{ uploadLoading ? 'Загрузка...' : 'Загрузить фото' }}
                </span>
              </button>
              <button
                type="button"
                @click="clearForm"
                class="clear-button"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;">
                  <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Очистить
              </button>
            </div>

            <div v-if="uploadError" class="error-message">
              <div class="error-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10.29 3.86L1.82 18C1.64539 18.3024 1.55299 18.6453 1.55201 18.9945C1.55103 19.3437 1.64151 19.6871 1.81445 19.9905C1.9874 20.2939 2.23675 20.5467 2.53773 20.7238C2.83871 20.9009 3.18082 20.9962 3.53 21H20.47C20.8192 20.9962 21.1613 20.9009 21.4623 20.7238C21.7633 20.5467 22.0126 20.2939 22.1856 19.9905C22.3585 19.6871 22.449 19.3437 22.448 18.9945C22.447 18.6453 22.3546 18.3024 22.18 18L13.71 3.86C13.5317 3.56611 13.2807 3.32312 12.9812 3.15448C12.6817 2.98585 12.3437 2.89725 12 2.89725C11.6563 2.89725 11.3183 2.98585 11.0188 3.15448C10.7193 3.32312 10.4683 3.56611 10.29 3.86Z" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 9V13" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 17H12.01" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="error-text">{{ uploadError }}</div>
            </div>
          </form>
        </div>
      </div>

      <!-- Список фото -->
      <div class="gallery-section">
        <div class="section-header">
          <div class="section-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 16L8.586 11.414C8.96106 11.0391 9.46967 10.8284 10 10.8284C10.5303 10.8284 11.0389 11.0391 11.414 11.414L16 16" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M14 14L15.586 12.414C15.9611 12.0391 16.4697 11.8284 17 11.8284C17.5303 11.8284 18.0389 12.0391 18.414 12.414L20 14" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M14 8H14.01" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="3" y="3" width="18" height="18" rx="2" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="section-header-content">
            <h2 class="section-title">Галерея фотографий</h2>
            <p class="section-subtitle">Всего загружено {{ photos.length }} фотографий</p>
          </div>
          <button
            @click="loadPhotos"
            class="refresh-button"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner small"></span>
            <span v-else>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 4V10H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M23 20V14H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M20.49 9C19.9828 7.56678 19.1209 6.2854 17.9845 5.27542C16.8482 4.26543 15.4745 3.55976 14 3.22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3.51 15C4.01717 16.4332 4.87915 17.7146 6.01547 18.7246C7.1518 19.7346 8.52547 20.4402 10 20.78" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
          </button>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p class="loading-text">Загружаем фотографии...</p>
        </div>

        <div v-else-if="error" class="error-state">
          <div class="error-icon large">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 8V12" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 16H12.01" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p class="error-title">Ошибка загрузки</p>
          <p class="error-description">{{ error }}</p>
          <button @click="loadPhotos" class="retry-button">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;">
              <path d="M1 4V10H7" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M23 20V14H17" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M20.49 9C19.9828 7.56678 19.1209 6.2854 17.9845 5.27542C16.8482 4.26543 15.4745 3.55976 14 3.22" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M3.51 15C4.01717 16.4332 4.87915 17.7146 6.01547 18.7246C7.1518 19.7346 8.52547 20.4402 10 20.78" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Повторить попытку
          </button>
        </div>

        <div v-else-if="photos.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M23 19C23 19.5304 22.7893 20.0391 22.4142 20.4142C22.0391 20.7893 21.5304 21 21 21H3C2.46957 21 1.96086 20.7893 1.58579 20.4142C1.21071 20.0391 1 19.5304 1 19V8C1 7.46957 1.21071 6.96086 1.58579 6.58579C1.96086 6.21071 2.46957 6 3 6H7L9 3H15L17 6H21C21.5304 6 22.0391 6.21071 22.4142 6.58579C22.7893 6.96086 23 7.46957 23 8V19Z" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 17C14.2091 17 16 15.2091 16 13C16 10.7909 14.2091 9 12 9C9.79086 9 8 10.7909 8 13C8 15.2091 9.79086 17 12 17Z" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p class="empty-title">Галерея пуста</p>
          <p class="empty-description">Будьте первым, кто загрузит фотографию!</p>
        </div>

        <div v-else class="photos-grid">
          <PhotoCard
            v-for="photo in photos"
            :key="photo.id"
            :photo="photo"
            @delete="handleDelete(photo.id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { usePhotos } from '@/composables/usePhotos';
import PhotoCard from '@/components/PhotoCard.vue';
import { api } from '@/api/api';
import { useToast } from 'vue-toastification';

const toast = useToast();
const { photos, loading, error, loadPhotos, deletePhoto } = usePhotos();

loadPhotos();

const form = ref({ title: '', description: '' });
const file = ref<File | null>(null);
const uploadLoading = ref(false);
const uploadError = ref<string | null>(null);

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const selectedFile = target.files?.[0];
  if (selectedFile) {
    if (selectedFile.size > 5 * 1024 * 1024) {
      uploadError.value = 'Файл слишком большой. Максимальный размер: 5 МБ';
      return;
    }
    file.value = selectedFile;
    uploadError.value = null;
  }
};

const handleFileDrop = (e: DragEvent) => {
  e.preventDefault();
  const droppedFile = e.dataTransfer?.files[0];
  if (droppedFile && droppedFile.type.startsWith('image/')) {
    if (droppedFile.size > 5 * 1024 * 1024) {
      uploadError.value = 'Файл слишком большой. Максимальный размер: 5 МБ';
      return;
    }
    file.value = droppedFile;
    uploadError.value = null;
  }
};

const clearForm = () => {
  form.value = { title: '', description: '' };
  file.value = null;
  uploadError.value = null;
  const fileInput = document.getElementById('file-input') as HTMLInputElement;
  if (fileInput) fileInput.value = '';
};

const handleSubmit = async () => {
  if (!file.value) {
    uploadError.value = 'Пожалуйста, выберите изображение';
    return;
  }

  if (!form.value.title.trim()) {
    uploadError.value = 'Пожалуйста, введите название';
    return;
  }

  uploadLoading.value = true;
  uploadError.value = null;

  const formData = new FormData();
  formData.append('title', form.value.title.trim());
  if (form.value.description.trim()) {
    formData.append('description', form.value.description.trim());
  }
  formData.append('file', file.value);

  try {
    await api.post('/photos/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    toast.success('✅ Фотография успешно загружена!');
    clearForm();
    await loadPhotos();

  } catch (err: any) {
    const msg = err.response?.data?.detail || 'Ошибка загрузки';
    uploadError.value = msg;
    toast.error(`❌ ${msg}`);
  } finally {
    uploadLoading.value = false;
  }
};

const handleDelete = async (id: string) => {
  if (!confirm('Вы уверены, что хотите удалить эту фотографию? Это действие нельзя отменить.')) {
    return;
  }

  try {
    await deletePhoto(id);
    toast.success('✅ Фотография удалена');
  } catch (err: any) {
    toast.error(`❌ ${err.message}`);
  }
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
  margin-bottom: 60px;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.hero-content {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
}

.hero-icon {
  margin-bottom: 20px;
  display: inline-block;
  background: rgba(255, 255, 255, 0.1);
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  backdrop-filter: blur(10px);
}

.hero-icon svg {
  stroke: white;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 16px;
  letter-spacing: -0.5px;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 40px;
  font-weight: 300;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 40px;
}

.stat {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-header {
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.section-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.section-icon svg {
  stroke: white;
}

.section-header-content {
  flex: 1;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.section-subtitle {
  font-size: 16px;
  color: #64748b;
  margin: 4px 0 0;
}

.refresh-button {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.refresh-button:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
  transform: rotate(90deg);
}

.refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-button svg {
  stroke: currentColor;
}

.upload-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  border: 1px solid #f1f5f9;
  margin-bottom: 60px;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label-text {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.label-required,
.label-optional {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.label-required {
  background: #fee2e2;
  color: #dc2626;
}

.label-optional {
  background: #f1f5f9;
  color: #64748b;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #94a3b8;
}

.input-hint {
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}

.file-upload-area {
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  background: #f8fafc;
}

.file-upload-area:hover {
  border-color: #667eea;
  background: #f1f5ff;
}

.file-upload-area.has-file {
  border-color: #10b981;
  background: #f0fdf4;
}

.upload-icon {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
}

.upload-icon svg {
  stroke: #94a3b8;
}

.upload-text {
  font-size: 16px;
  color: #1e293b;
  margin-bottom: 8px;
}

.browse-link {
  color: #667eea;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
}

.browse-link:hover {
  color: #5a67d8;
}

.file-name {
  font-weight: 600;
  color: #10b981;
}

.upload-hint {
  font-size: 14px;
  color: #64748b;
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 16px;
  margin-top: 24px;
}

.upload-button {
  flex: 1;
  padding: 16px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.upload-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.upload-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.button-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-button svg {
  stroke: white;
}

.clear-button {
  padding: 16px 32px;
  background: white;
  color: #64748b;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-button:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.clear-button svg {
  stroke: currentColor;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  margin-top: 16px;
}

.error-icon {
  flex-shrink: 0;
}

.error-icon svg {
  stroke: #dc2626;
}

.error-text {
  color: #dc2626;
  font-weight: 500;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

.spinner.small {
  width: 16px;
  height: 16px;
  border-width: 2px;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 3px solid #e2e8f0;
  border-radius: 50%;
  border-top-color: #667eea;
  margin: 0 auto 24px;
  animation: spin 1s linear infinite;
}

.loading-text {
  color: #64748b;
  font-size: 16px;
  font-weight: 500;
}

.error-state {
  text-align: center;
  padding: 80px 20px;
}

.error-icon.large {
  margin-bottom: 24px;
  display: flex;
  justify-content: center;
}

.error-icon.large svg {
  stroke: #94a3b8;
}

.error-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.error-description {
  color: #64748b;
  margin-bottom: 24px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.retry-button {
  padding: 12px 32px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.retry-button:hover {
  background: #5a67d8;
}

.retry-button svg {
  stroke: white;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  margin-bottom: 24px;
  opacity: 0.5;
  display: flex;
  justify-content: center;
}

.empty-icon svg {
  stroke: #cbd5e1;
}

.empty-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.empty-description {
  color: #64748b;
  max-width: 400px;
  margin: 0 auto;
}

.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  animation: fadeIn 0.5s ease-out;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .hero-stats {
    gap: 20px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .refresh-button {
    align-self: flex-end;
  }

  .upload-card {
    padding: 24px;
  }

  .photos-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 60px 20px;
  }

  .hero-title {
    font-size: 28px;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
