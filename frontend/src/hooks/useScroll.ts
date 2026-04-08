import { ref, nextTick } from 'vue';

export interface ScrollOptions {
  behavior?: ScrollBehavior;
  left?: number;
  top?: number;
}


export function useScroll() {
  const scrollRef = ref<HTMLElement | null>(null);


  const scrollToBottom = (smooth = true) => {
    nextTick(() => {
      if (scrollRef.value) {
        scrollRef.value.scrollTo({
          top: scrollRef.value.scrollHeight,
          behavior: smooth ? 'smooth' : 'auto',
        });
      }
    });
  };


  const scrollToTop = (smooth = true) => {
    nextTick(() => {
      if (scrollRef.value) {
        scrollRef.value.scrollTo({
          top: 0,
          behavior: smooth ? 'smooth' : 'auto',
        });
      }
    });
  };


  const scrollTo = (options: ScrollOptions) => {
    nextTick(() => {
      if (scrollRef.value) {
        scrollRef.value.scrollTo(options);
      }
    });
  };

  return {
    scrollRef,
    scrollToBottom,
    scrollToTop,
    scrollTo,
  };
}
