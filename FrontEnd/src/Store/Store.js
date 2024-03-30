import { create } from 'zustand';
import { link } from '../Links';
import axios from 'axios';

export const useUserStore = create((set) => ({
    isAuthenticated: false,
    loading: true, // Initialize loading as true
    error: null,
    user: null,
    loadUser: async () => {
      try {
        const response = await axios.get(`${link}/getuser`, {
          withCredentials: true,
        });
        set({ isAuthenticated: true, user: response.data.user });
      } catch (error) {
        set({ error: error.message });
      } finally {
        // Set loading to false regardless of success or failure
        set({ loading: false });
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
    loading: false,
    setLoading: (isLoading) => set({ loading: isLoading }),
}));

export const useFinanceStore = create((set)=>({
    FinanceData:null,
    setFinanceData:(data)=>{
        set({FinanceData:data});
    }
}))
