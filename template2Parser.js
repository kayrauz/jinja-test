const puppeteer = require('puppeteer');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

const rawArgs = process.argv.slice(2)
const name = rawArgs.pop()
const args = rawArgs

let completed = 0;

const finalfiles = []

args.forEach(async filePath => {
        const browser = await puppeteer.launch();
        
        const page = await browser.newPage();
      
        await page.setViewport({ width: 1192, height: 1686 });
      
        await page.goto(`file:///C:/Users/amnesia/Documents/projects/jinja-test/${filePath}`, { waitUntil: 'load' });
      
        await page.evaluate(() => {
          document.body.style.overflow = 'hidden';
          document.body.style.overflow = 'hidden'; 
          document.querySelectorAll('img').forEach(img => {
            if (!img.complete || img.naturalWidth === 0) {
              throw new Error(`Image not loaded: ${img.src}`);
            }
          });
      
          document.fonts.ready.then(() => {
            console.log('All fonts are loaded');
          });
        });

        const pdfFileName = filePath.replace(".html", ".pdf")
      
        await page.pdf({
          path: pdfFileName, 
          format: 'A4',      
          printBackground: true,
          scale: 1,
          margin: {
              top: '0mm',
              bottom: '0mm',
              left: '0mm',
              right: '0mm',
            },
        });
      
        console.log('PDF generated successfully');
      
        await browser.close().then(async () => {
          const input_file = pdfFileName
          const output_file = `${input_file.replace(".pdf", "-removed.pdf")}`
      
          const pdfBuffer = fs.readFileSync(input_file);
          const pdfDoc = await PDFDocument.load(pdfBuffer);

          finalfiles.push(output_file)
      
          const totalPages = pdfDoc.getPageCount();
      
          if (totalPages > 0) {
              pdfDoc.removePage(totalPages - 1);
              const modifiedPdfBytes = await pdfDoc.save();
              fs.writeFileSync(output_file, modifiedPdfBytes);
              console.log(`Last page removed. New file saved as: ${output_file}`);
          }
          completed++;

          if (completed === args.length) {
            mergePages(finalfiles[0], finalfiles[1], `${name.toUpperCase()}.pdf`)
          }
        })
})

async function mergePages(firstPdf, secondPdf, outputPdf) {
    const first = fs.readFileSync(firstPdf);
    const second = fs.readFileSync(secondPdf);

    const firstDoc = await PDFDocument.load(first);
    const secondDoc = await PDFDocument.load(second);

    const [firstPage] = await firstDoc.copyPages(secondDoc, [0]);

    firstDoc.addPage(firstPage);

    const modifiedPdf = await firstDoc.save();

    fs.writeFileSync(outputPdf, modifiedPdf);

    console.log(`First page added. New file saved as: ${outputPdf}`);
    
}

