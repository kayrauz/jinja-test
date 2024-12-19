const puppeteer = require('puppeteer');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

const rawArgs = process.argv.slice(2)
const raw = rawArgs.pop()
const validJsonStr = raw.replace(/'/g, '"');
const arr = JSON.parse(validJsonStr);
const studentInfo = { "name": arr[0], "test_center": arr[1], "school": arr[2] }
const args = rawArgs

let completed = 0;

const finalfiles = []
args.forEach(async filePath => {
  const browser = await puppeteer.launch();

  const page = await browser.newPage();

  await page.setViewport({ width: 1192, height: 1686 });

  await page.goto(`file:///C:/Users/amnesia/Documents/projects/jinja-test/template1-output/${filePath}`, { waitUntil: 'load' });

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
  const path = `./${studentInfo.test_center}/${studentInfo.school}`
  

  fs.mkdirSync(path, { recursive: true });

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

  await browser.close()
    .then(async () => {
      const input_file = pdfFileName
      const output_file = `${input_file}`

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
        const newList = finalfiles.sort((a, b) => {
          const pageA = parseInt(a.match(/page(\d+)(?:-\d+)?\.pdf/)[1], 10);  
          const pageB = parseInt(b.match(/page(\d+)(?:-\d+)?\.pdf/)[1], 10);
          return pageA - pageB; 
        })

        const fullPath = `${path}/${studentInfo['name'].toUpperCase()}.pdf`

        mergePages(newList[0], [newList[1], newList[2], newList[3], newList[4]], fullPath)
      }
    })
})

async function mergePages(firstPdf, secondPdf, outputPdf) {
  const first = fs.readFileSync(firstPdf);
  const firstDoc = await PDFDocument.load(first);


  for (const additionalPdfPath of secondPdf) {
    const additionalPdfBytes = fs.readFileSync(additionalPdfPath);
    const additionalPdfDoc = await PDFDocument.load(additionalPdfBytes);

    const [firstPage] = await firstDoc.copyPages(additionalPdfDoc, [0]);

    firstDoc.addPage(firstPage);
  }


  const modifiedPdf = await firstDoc.save();

  fs.writeFileSync(outputPdf, modifiedPdf);

  console.log(`First page added. New file saved as: ${outputPdf}`);

}