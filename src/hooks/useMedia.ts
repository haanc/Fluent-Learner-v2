import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

export const useMediaList = () => {
    return useQuery({
        queryKey: ['media'],
        queryFn: api.listMedia,
        refetchInterval: 2000 // Poll every 2 seconds to track download/processing status
    });
};

export const useMediaDetail = (id: string) => {
    return useQuery({
        queryKey: ['media', id],
        queryFn: () => api.getMedia(id),
        enabled: !!id
    });
};

export const useSubtitleSegments = (mediaId: string | null) => {
    return useQuery({
        queryKey: ['segments', mediaId],
        queryFn: () => api.listSegments(mediaId!),
        enabled: !!mediaId
    });
};
