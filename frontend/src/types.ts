// src/types.ts
export interface Photo {
  id: string;
  title: string;
  description: string | null;
  filename: string;
  url: string;
  thumb_url: string | null;
  upload_date: string;
}
