// src/composables/usePhotos.ts
import { ref } from 'vue';
import { api } from '@/api/api';

interface Photo {
  id: string;
  title: string;
  description: string | null;
  filename: string;
  url: string;
  thumb_url: string | null;
  upload_date: string;
}

export function usePhotos() {
  const photos = ref<Photo[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const loadPhotos = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.get<Photo[]>('/photos');
      photos.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load photos';
    } finally {
      loading.value = false;
    }
  };

  const deletePhoto = async (id: string) => {
    try {
      await api.delete(`/photos/${id}`);
      photos.value = photos.value.filter(p => p.id !== id);
    } catch (err: any) {
      throw new Error(err.response?.data?.detail || 'Delete failed');
    }
  };

  return {
    photos,
    loading,
    error,
    loadPhotos,
    deletePhoto
  };
}
