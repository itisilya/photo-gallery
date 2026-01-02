<template>
  <div class="photo-detail-view">
    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showDeleteModal" class="delete-modal-overlay" @click.self="closeDeleteModal">
      <div class="delete-modal">
        <div class="modal-icon">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10.29 3.86L1.82 18C1.64539 18.3024 1.55299 18.6453 1.55201 18.9945C1.55103 19.3437 1.64151 19.6871 1.81445 19.9905C1.9874 20.2939 2.23675 20.5467 2.53773 20.7238C2.83871 20.9009 3.18082 20.9962 3.53 21H20.47C20.8192 20.9962 21.1613 20.9009 21.4623 20.7238C21.7633 20.5467 22.0126 20.2939 22.1856 19.9905C22.3585 19.6871 22.449 19.3437 22.448 18.9945C22.447 18.6453 22.3546 18.3024 22.18 18L13.71 3.86C13.5317 3.56611 13.2807 3.32312 12.9812 3.15448C12.6817 2.98585 12.3437 2.89725 12 2.89725C11.6563 2.89725 11.3183 2.98585 11.0188 3.15448C10.7193 3.32312 10.4683 3.56611 10.29 3.86Z" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 9V13" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 17H12.01" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>

        <div class="modal-content">
          <h3 class="modal-title">Удалить фотографию?</h3>

          <div class="modal-preview" v-if="photo">
            <img :src="photo.url" :alt="photo.title" class="preview-image" />
            <div class="preview-info">
              <div class="preview-title">{{ photo.title }}</div>
              <div class="preview-date">{{ formatDate(photo.upload_date) }}</div>
            </div>
          </div>

          <p class="modal-warning">
            Вы уверены, что хотите удалить эту фотографию?
            <br>
            <strong>Это действие нельзя отменить.</strong>
          </p>
        </div>

        <div class="modal-actions">
          <button @click="closeDeleteModal" class="modal-button modal-button--cancel">
            Отмена
          </button>
          <button @click="confirmDelete" class="modal-button modal-button--delete" :disabled="deleting">
            <span v-if="deleting" class="button-spinner"></span>
            <span v-else>Удалить навсегда</span>
          </button>
        </div>
      </div>
    </div>

    <div class="detail-container">
      <!-- Навигация -->
      <nav class="detail-nav">
        <router-link to="/" class="back-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 12H5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Назад в галерею
        </router-link>
        <div class="nav-actions">
          <button @click="copyLink" class="nav-action-button" title="Скопировать ссылку">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 16C8 18.2091 9.79086 20 12 20H18C20.2091 20 22 18.2091 22 16V12C22 9.79086 20.2091 8 18 8H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M16 8C16 5.79086 14.2091 4 12 4H6C3.79086 4 2 5.79086 2 8V12C2 14.2091 3.79086 16 6 16H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button @click="downloadImage" class="nav-action-button" title="Скачать изображение">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </nav>

      <!-- Основное содержимое -->
      <div class="detail-content">
        <!-- Загрузка -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner large"></div>
          <p class="loading-text">Загружаем фотографию...</p>
        </div>

        <!-- Ошибка -->
        <div v-else-if="!photo && !loading" class="error-state">
          <div class="error-icon-container">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 8V12" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 16H12.01" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="error-title">Фотография не найдена</h2>
          <p class="error-description">Возможно, она была удалена или перемещена</p>
          <router-link to="/" class="home-button">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Вернуться в галерею
          </router-link>
        </div>

        <!-- Успешная загрузка -->
        <div v-else class="photo-content">
          <div class="photo-display-section">
            <div class="image-container">
              <img
                :src="photo.url"
                :alt="editing.title || photo.title"
                class="detail-image"
                @load="imageLoaded = true"
                @error="onImageError"
                :class="{ 'loaded': imageLoaded }"
                :style="{ transform: `scale(${zoomLevel})` }"
              />
              <div v-if="!imageLoaded" class="image-loading">
                <div class="loading-spinner"></div>
              </div>
              <div v-if="imageError" class="image-fallback">
                <div class="fallback-icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M23 19C23 19.5304 22.7893 20.0391 22.4142 20.4142C22.0391 20.7893 21.5304 21 21 21H3C2.46957 21 1.96086 20.7893 1.58579 20.4142C1.21071 20.0391 1 19.5304 1 19V8C1 7.46957 1.21071 6.96086 1.58579 6.58579C1.96086 6.21071 2.46957 6 3 6H7L9 3H15L17 6H21C21.5304 6 22.0391 6.21071 22.4142 6.58579C22.7893 6.96086 23 7.46957 23 8V19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 17C14.2091 17 16 15.2091 16 13C16 10.7909 14.2091 9 12 9C9.79086 9 8 10.7909 8 13C8 15.2091 9.79086 17 12 17Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <p class="fallback-text">Не удалось загрузить изображение</p>
              </div>
              <div class="image-actions">
                <button @click="zoomIn" class="image-action-button" :disabled="zoomLevel >= 2">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M10 7V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 10H13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button @click="zoomOut" class="image-action-button" :disabled="zoomLevel <= 0.5">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 10H13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button @click="resetZoom" class="image-action-button" :disabled="zoomLevel === 1">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3 6H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div class="photo-info-section">
            <div class="info-card">
              <div class="info-header">
                <div class="title-actions">
                  <h1 v-if="!editingMode" class="photo-title">{{ photo.title }}</h1>
                  <input
                    v-else
                    v-model="editing.title"
                    type="text"
                    class="photo-title-input"
                    placeholder="Введите название"
                    :class="{ 'error': editingErrors.title }"
                    @keyup.enter="saveEdits"
                  />
                  <button
                    @click="toggleEditMode"
                    class="edit-button"
                    :title="editingMode ? 'Отменить изменения' : 'Редактировать'"
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M11 5H6C4.89543 5 4 5.89543 4 7V18C4 19.1046 4.89543 20 6 20H17C18.1046 20 19 19.1046 19 18V13M16 4V9M20 8H16M16 8H12M16 8V12M16 8L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
                <div class="photo-id">ID: {{ photo.id }}</div>
              </div>

              <div class="description-section">
                <div class="section-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 16V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 8H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Описание
                </div>
                <p v-if="!editingMode && photo.description" class="description-text">{{ photo.description }}</p>
                <p v-else-if="!editingMode && !photo.description" class="description-placeholder">Нет описания</p>
                <textarea
                  v-else
                  v-model="editing.description"
                  class="description-input"
                  placeholder="Введите описание (необязательно)"
                />
              </div>

              <div class="metadata-section">
                <div class="section-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Информация
                </div>

                <div class="metadata-grid">
                  <div class="metadata-item">
                    <div class="metadata-label">Дата загрузки</div>
                    <div class="metadata-value">{{ formatDate(photo.upload_date) }}</div>
                  </div>

                  <div class="metadata-item">
                    <div class="metadata-label">Имя файла</div>
                    <div class="metadata-value filename">{{ photo.filename }}</div>
                  </div>

                  <div class="metadata-item">
                    <div class="metadata-label">Тип файла</div>
                    <div class="metadata-value filetype">{{ getFileType(photo.filename) }}</div>
                  </div>

                  <div class="metadata-item">
                    <div class="metadata-label">Статус</div>
                    <div class="metadata-value status">
                      <span class="status-dot"></span>
                      Загружено
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="editingMode" class="edit-actions">
                <button @click="saveEdits" class="save-button" :disabled="saving">
                  <span v-if="saving" class="button-spinner"></span>
                  <span v-else>Сохранить изменения</span>
                </button>
                <button @click="cancelEdit" class="cancel-button">Отмена</button>
              </div>

              <div class="danger-zone">
                <div class="section-label danger">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10.29 3.86L1.82 18C1.64539 18.3024 1.55299 18.6453 1.55201 18.9945C1.55103 19.3437 1.64151 19.6871 1.81445 19.9905C1.9874 20.2939 2.23675 20.5467 2.53773 20.7238C2.83871 20.9009 3.18082 20.9962 3.53 21H20.47C20.8192 20.9962 21.1613 20.9009 21.4623 20.7238C21.7633 20.5467 22.0126 20.2939 22.1856 19.9905C22.3585 19.6871 22.449 19.3437 22.448 18.9945C22.447 18.6453 22.3546 18.3024 22.18 18L13.71 3.86C13.5317 3.56611 13.2807 3.32312 12.9812 3.15448C12.6817 2.98585 12.3437 2.89725 12 2.89725C11.6563 2.89725 11.3183 2.98585 11.0188 3.15448C10.7193 3.32312 10.4683 3.56611 10.29 3.86Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 9V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 17H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Опасная зона
                </div>
                <p class="danger-description">
                  Удаление фотографии необратимо. После удаления восстановить данные будет невозможно.
                </p>
                <button @click="openDeleteModal" class="delete-button">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M19 6V20C19 21 18 22 17 22H7C6 22 5 21 5 20V6M8 6V4C8 3 9 2 10 2H14C15 2 16 3 16 4V6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M10 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M14 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Удалить фотографию
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from '@/api/api';
import { Photo } from '@/types';
import { useToast } from 'vue-toastification';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const photo = ref<Photo | null>(null);
const loading = ref(true);
const imageLoaded = ref(false);
const imageError = ref(false);
const zoomLevel = ref(1);
const showDeleteModal = ref(false);
const deleting = ref(false);
const editingMode = ref(false);
const saving = ref(false);

// Редактируемые поля
const editing = ref({
  title: '',
  description: ''
});

const editingErrors = ref({
  title: false
});

const loadPhoto = async () => {
  const id = route.params.id as string;
  if (!id) {
    loading.value = false;
    return;
  }

  try {
    const response = await api.get<Photo>(`/photos/${id}`);
    photo.value = response.data;
    resetEditing();
  } catch (err: any) {
    console.error('Ошибка загрузки фотографии:', err);
    toast.error('Не удалось загрузить фотографию');
  } finally {
    loading.value = false;
  }
};

const resetEditing = () => {
  if (!photo.value) return;
  editing.value.title = photo.value.title;
  editing.value.description = photo.value.description || '';
  editingErrors.value.title = false;
};

const toggleEditMode = () => {
  if (!editingMode.value) {
    resetEditing();
  }
  editingMode.value = !editingMode.value;
};

const cancelEdit = () => {
  editingMode.value = false;
};

const saveEdits = async () => {
  if (!photo.value) return;

  // Валидация
  editingErrors.value.title = !editing.value.title.trim();
  if (editingErrors.value.title) {
    toast.error('Название не может быть пустым');
    return;
  }

  saving.value = true;

  try {
    const updatedData = {
      title: editing.value.title.trim(),
      description: editing.value.description.trim() || null
    };

    await api.patch(`/photos/${photo.value.id}`, updatedData);

    // Обновляем локальное состояние
    photo.value.title = updatedData.title;
    photo.value.description = updatedData.description;

    toast.success('✅ Изменения сохранены');
    editingMode.value = false;
  } catch (err: any) {
    console.error('Ошибка сохранения:', err);
    const msg = err.response?.data?.detail || 'Не удалось сохранить изменения';
    toast.error(`❌ ${msg}`);
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadPhoto();
});

const formatDate = (isoString: string) => {
  const date = new Date(isoString);
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

const getFileType = (filename: string) => {
  const ext = filename.split('.').pop()?.toUpperCase();
  return ext ? `Файл .${ext}` : 'Изображение';
};

const onImageError = () => {
  imageError.value = true;
  toast.warning('Не удалось загрузить изображение');
};

const zoomIn = () => {
  if (zoomLevel.value < 2) {
    zoomLevel.value += 0.25;
  }
};

const zoomOut = () => {
  if (zoomLevel.value > 0.5) {
    zoomLevel.value -= 0.25;
  }
};

const resetZoom = () => {
  zoomLevel.value = 1;
};

const copyLink = () => {
  const url = window.location.href;
  navigator.clipboard.writeText(url)
    .then(() => toast.success('Ссылка скопирована в буфер обмена'))
    .catch(() => toast.error('Не удалось скопировать ссылку'));
};

const downloadImage = () => {
  if (!photo.value) return;

  try {
    // ✅ Обход CORS: не используем fetch — просто эмулируем клик по <a download>
    const link = document.createElement('a');
    link.href = photo.value.url;
    link.download = photo.value.filename || `photo-${photo.value.id}.jpg`;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    toast.success('Скачивание начато');
  } catch (err) {
    console.error('Ошибка скачивания:', err);
    toast.error('Не удалось скачать изображение');
  }
};

const openDeleteModal = () => {
  showDeleteModal.value = true;
  document.body.style.overflow = 'hidden';
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  document.body.style.overflow = 'auto';
};

const confirmDelete = async () => {
  if (!photo.value) return;

  deleting.value = true;

  try {
    await api.delete(`/photos/${photo.value.id}`);
    toast.success('✅ Фотография удалена');
    closeDeleteModal();
    router.push('/');
  } catch (err: any) {
    const msg = err.response?.data?.detail || 'Ошибка удаления';
    toast.error(`❌ ${msg}`);
  } finally {
    deleting.value = false;
  }
};
</script>

<style scoped>
.photo-detail-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  padding: 20px;
}

/* ✅ Фиолетовый фон панели навигации */
.detail-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #6f5fbe 0%, #5b4a9e 100%);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(111, 95, 190, 0.3);
}

.back-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  font-size: 14px;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateX(-2px);
}

.back-button svg {
  stroke: currentColor;
}

.nav-actions {
  display: flex;
  gap: 8px;
}

.nav-action-button {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.15);
  color: white;
  backdrop-filter: blur(10px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.nav-action-button:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
}

.nav-action-button svg {
  stroke: currentColor;
}

.detail-content {
  min-height: calc(100vh - 120px);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 3px solid #e2e8f0;
  border-radius: 50%;
  border-top-color: #667eea;
  animation: spin 1s linear infinite;
  margin-bottom: 24px;
}

.loading-spinner.large {
  width: 80px;
  height: 80px;
  border-width: 4px;
}

.loading-text {
  color: #64748b;
  font-size: 18px;
  font-weight: 500;
}

.error-state {
  text-align: center;
  padding: 100px 20px;
}

.error-icon-container {
  margin-bottom: 24px;
}

.error-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}

.error-description {
  color: #64748b;
  margin-bottom: 32px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.home-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.home-button:hover {
  background: #5a67d8;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.home-button svg {
  stroke: currentColor;
}

.photo-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 32px;
}

@media (max-width: 1024px) {
  .photo-content {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}

.photo-display-section {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid #f1f5f9;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
}

.image-container {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.detail-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s;
  opacity: 0;
}

.detail-image.loaded {
  opacity: 1;
}

.image-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
}

.image-fallback {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  color: #94a3b8;
}

.fallback-icon {
  margin-bottom: 16px;
}

.fallback-icon svg {
  stroke: #cbd5e1;
}

.fallback-text {
  font-size: 16px;
  font-weight: 500;
}

.image-actions {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 8px;
  border-radius: 12px;
  border: 1px solid rgba(226, 232, 240, 0.5);
}

.image-action-button {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.image-action-button:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #1e293b;
}

.image-action-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.image-action-button svg {
  stroke: currentColor;
}

.photo-info-section {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.info-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
}

.info-header {
  margin-bottom: 32px;
}

.photo-title {
  font-size: 28px;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.photo-id {
  font-size: 12px;
  color: #94a3b8;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
  letter-spacing: 0.5px;
}

.description-section,
.metadata-section,
.danger-zone {
  margin-bottom: 32px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.section-label.danger {
  color: #dc2626;
}

.section-label svg {
  stroke: currentColor;
}

.description-text {
  color: #475569;
  line-height: 1.7;
  font-size: 16px;
  margin: 0;
}

.description-placeholder {
  color: #94a3b8;
  font-style: italic;
  margin: 0;
}

.metadata-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.metadata-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f8fafc;
}

.metadata-label {
  font-size: 14px;
  color: #64748b;
}

.metadata-value {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.metadata-value.filename {
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
  font-size: 12px;
  color: #64748b;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.metadata-value.filetype {
  color: #667eea;
  font-weight: 600;
}

.metadata-value.status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #10b981;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.danger-description {
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 20px 0;
}

.delete-button {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.delete-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(220, 38, 38, 0.3);
}

.delete-button:active {
  transform: translateY(0);
}

.delete-button svg {
  stroke: currentColor;
}

/* === Стили для редактирования === */
.title-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.photo-title-input {
  flex: 1;
  font-size: 28px;
  font-weight: 800;
  color: #1e293b;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 16px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.photo-title-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.photo-title-input.error {
  border-color: #ef4444;
}

.edit-button {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #e2e8f0;
  color: #64748b;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.edit-button:hover {
  background: #cbd5e1;
  color: #475569;
  transform: rotate(90deg);
}

.edit-button svg {
  stroke: currentColor;
  stroke-width: 2;
}

.description-input {
  width: 100%;
  min-height: 100px;
  padding: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
  font-size: 16px;
  line-height: 1.6;
  color: #1e293b;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.description-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.edit-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
}

.save-button,
.cancel-button {
  flex: 1;
  padding: 14px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.save-button {
  background: linear-gradient(135deg, #6f5fbe 0%, #5b4a9e 100%);
  color: white;
  border: none;
}

.save-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(111, 95, 190, 0.4);
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-button {
  background: #f1f5f9;
  color: #64748b;
  border: 2px solid #e2e8f0;
}

.cancel-button:hover {
  background: #e2e8f0;
  transform: translateY(-1px);
}

/* === Модальное окно === */
.delete-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.delete-modal {
  background: white;
  border-radius: 24px;
  max-width: 500px;
  width: 100%;
  overflow: hidden;
  box-shadow: 0 32px 64px rgba(0, 0, 0, 0.25);
  animation: modalSlideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-icon {
  display: flex;
  justify-content: center;
  padding: 40px 0 20px;
  background: linear-gradient(to bottom, #fef2f2, white);
}

.modal-content {
  padding: 0 32px 24px;
}

.modal-title {
  text-align: center;
  font-size: 24px;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 24px 0;
}

.modal-preview {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid #f1f5f9;
}

.preview-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.preview-info {
  flex: 1;
}

.preview-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.preview-date {
  font-size: 12px;
  color: #64748b;
}

.modal-warning {
  text-align: center;
  color: #475569;
  line-height: 1.6;
  margin: 0;
  padding: 16px;
  background: #fef2f2;
  border-radius: 12px;
  border: 1px solid #fee2e2;
}

.modal-warning strong {
  color: #dc2626;
}

.modal-actions {
  display: flex;
  gap: 12px;
  padding: 24px 32px 32px;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
}

.modal-button {
  flex: 1;
  padding: 16px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
}

.modal-button--cancel {
  background: white;
  color: #64748b;
  border-color: #e2e8f0;
}

.modal-button--cancel:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

.modal-button--delete {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
}

.modal-button--delete:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(220, 38, 38, 0.3);
}

.modal-button--delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.button-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

@media (max-width: 768px) {
  .photo-detail-view {
    padding: 16px;
  }

  .detail-nav {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .back-button {
    justify-content: center;
  }

  .nav-actions {
    justify-content: center;
  }

  .photo-content {
    gap: 16px;
  }

  .info-card {
    padding: 24px;
  }

  .photo-title {
    font-size: 24px;
  }

  .image-actions {
    bottom: 16px;
    right: 16px;
  }

  .modal-actions {
    flex-direction: column;
  }

  .modal-button {
    width: 100%;
  }

  .delete-modal {
    max-width: 90%;
  }

  .title-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .photo-title-input {
    font-size: 24px;
  }
}
</style>
