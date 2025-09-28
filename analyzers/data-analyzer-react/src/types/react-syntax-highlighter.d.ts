// Custom type declarations for react-syntax-highlighter
declare module 'react-syntax-highlighter' {
  import { ComponentType, ReactNode } from 'react';

  export interface SyntaxHighlighterProps {
    language?: string;
    style?: any;
    customStyle?: any;
    showLineNumbers?: boolean;
    wrapLines?: boolean;
    PreTag?: string | ComponentType<any>;
    children?: ReactNode;
    [key: string]: any;
  }

  export const Prism: ComponentType<SyntaxHighlighterProps>;
}

declare module 'react-syntax-highlighter/dist/esm/styles/prism' {
  export const oneDark: any;
}

declare module 'react-syntax-highlighter/dist/cjs/index.js' {
  export const Prism: any;
}
