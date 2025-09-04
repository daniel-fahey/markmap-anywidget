import { Transformer } from 'markmap-lib';
import { Markmap, deriveOptions, refreshHook } from 'markmap-view';

function render({ model, el }) {
  const markdown = model.get('markdown_content');
  
  // Clear and setup
  el.innerHTML = '';
  el.className = 'markmap-widget';

  // Create SVG container
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.style.cssText = 'display:block;width:100%;height:100%;background:transparent';
  el.appendChild(svg);

  // Function to update theme
  const updateTheme = () => {
    // Remove existing theme classes
    el.classList.remove('markmap-dark');
    
    // Add dark theme class if system prefers dark mode
    if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) {
      el.classList.add('markmap-dark');
    }
  };

  // Set initial theme
  updateTheme();

  // Listen for theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  const handleThemeChange = (e) => {
    updateTheme();
    // Re-render the markmap to apply new theme
    if (el._markmap) {
      el._markmap.renderData(el._markmap.state.data);
    }
  };
  
  // Add event listener for theme changes
  mediaQuery.addEventListener('change', handleThemeChange);

  // Initialize markmap
  const initMarkmap = async () => {
    try {
      // Transform markdown to detect features
      const transformer = new Transformer();
      let { root, features, frontmatter } = transformer.transform(markdown);
      
      // Assets are bundled, no need to load them separately
      // The transformer will handle feature detection automatically
      
      // Re-transform after assets are loaded
      const finalResult = transformer.transform(markdown);
      root = finalResult.root;
      frontmatter = finalResult.frontmatter;
      
      // Create and configure markmap
      const markmapOptions = deriveOptions(frontmatter?.markmap);
      const mm = new Markmap(svg, markmapOptions);
      
      // Store reference to markmap on the element for theme updates
      el._markmap = mm;
      
      // Render the mindmap
      await mm.setData(root);
      await mm.fit();
      mm.renderData(root);
      
    } catch (error) {
      console.error('Markmap initialization failed:', error);
      
      // Provide detailed error information for debugging
      const errorDetails = {
        message: error.message || 'Unknown error',
        stack: error.stack,
        markdown: markdown?.substring(0, 100) + '...' // First 100 chars for context
      };
      
      console.error('Error details:', errorDetails);
      
      el.innerHTML = `
        <div style="color: red; padding: 20px; font-family: monospace;">
          <strong>Markmap failed to load</strong><br>
          Error: ${error.message || 'Unknown error'}<br>
          <small>Check browser console for details</small>
        </div>
      `;
    }
  };

  // Initialize after container is ready
  requestAnimationFrame(initMarkmap);
}

export default { render };