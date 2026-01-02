<template>
  <div class="photo-card" @click="goToDetail">
    <div class="card-header">
      <div class="upload-time">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        {{ formatDate(photo.upload_date) }}
      </div>
      <button
        @click.stop="onDelete"
        class="delete-button"
        :title="'Удалить фотографию'"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M19 6V20C19 21 18 22 17 22H7C6 22 5 21 5 20V6M8 6V4C8 3 9 2 10 2H14C15 2 16 3 16 4V6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M10 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M14 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <div class="image-container">
      <div class="image-wrapper">
      <img
        :src="photo.thumb_url || photo.url"
        :alt="photo.title"
        class="photo-image"
        loading="lazy"
        @load="imageLoaded = true"
        @error="imageError = true"
      />
        <div v-if="!imageLoaded && !imageError" class="image-skeleton">
          <div class="skeleton-animation"></div>
        </div>
        <div v-if="imageError" class="image-error">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 8V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Ошибка загрузки</span>
        </div>
      </div>
      <div class="image-overlay">
        <button class="view-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Просмотр
        </button>
      </div>
    </div>

    <div class="card-content">
      <div class="photo-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="title-icon">
          <path d="M4 16L8.586 11.414C8.96106 11.0391 9.46967 10.8284 10 10.8284C10.5303 10.8284 11.0389 11.0391 11.414 11.414L16 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M14 14L15.586 12.414C15.9611 12.0391 16.4697 11.8284 17 11.8284C17.5303 11.8284 18.0389 12.0391 18.414 12.414L20 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M14 8H14.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h3 class="title-text">{{ photo.title }}</h3>
      </div>

      <div v-if="photo.description" class="photo-description">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="description-icon">
          <path d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.3944 16.7118 18.3098 17.8992 16.9674 18.7293C15.6251 19.5594 14.0782 19.9994 12.5 20C11.1801 20.0034 9.87812 19.6951 8.7 19.1L3 21L4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5C4.00061 9.92179 4.44061 8.37488 5.27072 7.03258C6.10083 5.69028 7.28825 4.6056 8.7 3.90003C9.87812 3.30496 11.1801 2.99659 12.5 3.00003H13C15.0843 3.11502 17.053 3.99479 18.5291 5.47089C20.0052 6.94699 20.885 8.91568 21 11V11.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p class="description-text">{{ truncateDescription(photo.description) }}</p>
      </div>

      <div class="photo-footer">
        <div class="file-info">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C4.9 2 4.01 2.9 4.01 4L4 20C4 21.1 4.89 22 5.99 22H18C19.1 22 20 21.1 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="filename">{{ getFileExtension(photo.filename) }}</span>
        </div>
        <div class="photo-id">
          ID: {{ photo.id.slice(0, 8) }}...
        </div>
      </div>
    </div>

    <div class="card-hover-effect"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps<{ photo: Photo }>();
const emit = defineEmits(['delete']);
const router = useRouter();
const imageLoaded = ref(false);
const imageError = ref(false);

const goToDetail = () => {
  router.push(`/photos/${props.photo.id}`);
};

const onDelete = () => {
  emit('delete');
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - date.getTime());
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 0) {
    return 'Сегодня';
  } else if (diffDays === 1) {
    return 'Вчера';
  } else if (diffDays < 7) {
    return `${diffDays} дня назад`;
  } else {
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  }
};

const truncateDescription = (description: string) => {
  if (description.length > 100) {
    return description.substring(0, 100) + '...';
  }
  return description;
};

const getFileExtension = (filename: string) => {
  const ext = filename.split('.').pop()?.toUpperCase();
  return ext || 'IMG';
};

interface Photo {
  id: string;
  title: string;
  description: string | null;
  filename: string;
  url: string;
  thumb_url: string | null;
  upload_date: string;
}
</script>

<style scoped>
.photo-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  border: 1px solid #f1f5f9;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.photo-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15);
  border-color: #e2e8f0;
}

.photo-card:hover .card-hover-effect {
  opacity: 1;
  transform: scale(1.05);
}

.card-hover-effect {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.03), rgba(118, 75, 162, 0.03));
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.3s, transform 0.3s;
  pointer-events: none;
  z-index: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px 12px;
  position: relative;
  z-index: 1;
  background: white;
}

.upload-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.upload-time svg {
  stroke: #94a3b8;
}

.delete-button {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 2px solid #fee2e2;
  background: white;
  color: #dc2626;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.delete-button:hover {
  background: #fef2f2;
  border-color: #fecaca;
  transform: scale(1.1);
}

.delete-button:active {
  transform: scale(0.95);
}

.delete-button svg {
  stroke: currentColor;
}

.image-container {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
  margin: 0 20px;
  border-radius: 12px;
  z-index: 1;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.photo-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  display: block;
}

.photo-card:hover .photo-image {
  transform: scale(1.05);
}

.image-skeleton {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 12px;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.image-error {
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
  border-radius: 12px;
  gap: 8px;
}

.image-error svg {
  stroke: #cbd5e1;
}

.image-error span {
  font-size: 14px;
  font-weight: 500;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.4), transparent 40%);
  opacity: 0;
  transition: opacity 0.3s;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 20px;
  border-radius: 12px;
  pointer-events: none;
}

.photo-card:hover .image-overlay {
  opacity: 1;
}

.view-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.95);
  color: #1e293b;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  transform: translateY(10px);
  opacity: 0;
  pointer-events: auto;
  backdrop-filter: blur(10px);
}

.photo-card:hover .view-button {
  transform: translateY(0);
  opacity: 1;
}

.view-button:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
  z-index: 1;
  background: white;
}

.photo-title {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 4px;
}

.title-icon {
  flex-shrink: 0;
  stroke: #667eea;
  margin-top: 2px;
}

.title-text {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.4;
  flex: 1;
}

.photo-description {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: #f8fafc;
  padding: 12px;
  border-radius: 8px;
  margin: 4px 0;
}

.description-icon {
  flex-shrink: 0;
  stroke: #94a3b8;
  margin-top: 1px;
}

.description-text {
  margin: 0;
  font-size: 14px;
  color: #475569;
  line-height: 1.5;
  flex: 1;
}

.photo-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 500;
}

.file-info svg {
  stroke: #94a3b8;
}

.filename {
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
}

.photo-id {
  font-size: 11px;
  color: #cbd5e1;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
  letter-spacing: 0.5px;
  user-select: none;
}

@media (max-width: 768px) {
  .photo-card {
    border-radius: 16px;
  }

  .card-header,
  .card-content {
    padding: 16px;
  }

  .image-container {
    margin: 0 16px;
    border-radius: 10px;
  }

  .title-text {
    font-size: 16px;
  }

  .description-text {
    font-size: 13px;
  }
}
</style>
