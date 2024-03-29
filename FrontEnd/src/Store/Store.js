import { create } from 'zustand';
import { link } from '../Links';
import axios from 'axios';

export const useUserStore = create((set) => ({
  isAuthenticated: false,
  loading: false,
  error: null,
  user: null,
  loadUser: async () => {
    try {
      set({ loading: true });
      const response = await axios.get(`${link}/getuser`, {
        withCredentials: true,
      });
      set({ isAuthenticated: true, loading: false, user: response.data.user });
    } catch (error) {
      set({ loading: false, error: error.message, isAuthenticated: false });
    }
  },
  setUser: (userData) => {
    set({ user: userData, isAuthenticated: true });
  },
}));

export const useDarkModeStore = create((set)=>({
    mode:false,
    setMode:(mode)=>{
        set({ mode: mode });
    }
}));


export const useLoader = create((set)=>({
    loading:false,
    setLoading:(isLoading)=>{
        set({ loading: isLoading });
    }
}))
