/**
 * markmap-anywidget - anywidget integration for markmap
 *
 * Based on markmap by Gerald <gera2ld@live.com>
 * @see https://github.com/markmap/markmap
 */

import { Transformer } from 'markmap-lib';
import { Markmap, deriveOptions } from 'markmap-view';

interface Model {
  get(key: string): string;
}

interface WidgetProps {
  model: Model;
  el: HTMLElement;
}

function render({ model, el }: WidgetProps): void {
  const markdown = model.get('markdown_content');

  el.innerHTML = '';
  el.className = 'markmap-widget';

  // Create SVG container
  // Pattern from markmap-view/src/view.ts: Markmap constructor
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.style.cssText = 'display:block;width:100%;height:100%;background:transparent';
  el.appendChild(svg);

  // Theme handling
  const updateTheme = (): void => {
    const isDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches;
    el.classList.toggle('markmap-dark', isDark);
  };
  updateTheme();

  // Listen for theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  mediaQuery.addEventListener('change', () => {
    updateTheme();
    if ((el as any)._markmap) {
      (el as any)._markmap.renderData((el as any)._markmap.state.data);
    }
  });

  // Initialise markmap
  // Pattern from markmap-cli and markmap-vscode
  requestAnimationFrame(async () => {
    try {
      // Transformer pattern from markmap-lib/src/transform.ts
      const transformer = new Transformer();
      const { root, frontmatter } = transformer.transform(markdown);

      // Markmap.create pattern from markmap-view/src/view.ts
      const mm = new Markmap(svg, deriveOptions(frontmatter?.markmap));
      (el as any)._markmap = mm;

      await mm.setData(root);
      await mm.fit();
    } catch (error: any) {
      console.error('Markmap failed:', error);
      el.innerHTML = `<div style="color:red;padding:20px">Error: ${error.message}</div>`;
    }
  });
}

export default { render };
