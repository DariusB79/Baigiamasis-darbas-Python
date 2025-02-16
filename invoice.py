from datetime import datetime

invoice_html_data = f"""

<!DOCTYPE html>
<html xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" lang="en">
    <body style="font-family:Arial Unicode MS, Helvetica , Sans-Serif;">
        <table style="table-layout: fixed; width: 100%;">
            <tbody>
                <tr>
                    <td class="">
                        <div>
                            <img src="file:///C:/Users/HP/OneDrive/Desktop/phyton_mokymai/Paskaitos/_baigiamasis_darbas/logo.jpg" alt="Company Logo" style="max-width: 100%;">
                        </div>
                    </td>
                    <td width="15%">
                        
                    </td>
                    <td>    
                        <table class="tbl-padded">
                            <caption style="text-transform: uppercase; text-align: left; font-size: 30pt;">
                                <strong>
                                    Invoice
                                </strong>
                            </caption> 
                            <tbody>
                                <tr>
                                    <td style="padding:5px;">
                                        <strong >Invoice No.</strong>
                                    </td>
                                    <td style="padding:5px;">
                                        <div>
                                            INV-24
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:5px;">
                                        <strong >Date Issued </strong>                            
                                    </td>
                                    <td style="padding:5px;">
                                        {datetime.now().strftime("%Y-%m-%d")}
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:5px;">
                                        <strong >Due Date</strong>                            
                                    </td>
                                    <td style="padding:5px;">
                                        August 10, 2018
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:5px;">
                                        <strong >Currency</strong>                                
                                    </td>
                                    <td style="padding:5px;">
                                        USD - US Dollar
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <div style="padding-top: 1cm; padding-bottom: 1cm;">
            <table style="table-layout: fixed; width: 100%;">
                <tbody>
                    <tr>
                        <td>
                            <div style="padding-bottom: 10px;">
                                <strong style="text-transform: uppercase;">From</strong>
                            </div>
                            <div>
                                Wolters Kluwer India Pvt. Ltd. <br>
                                A-202, 2nd Floor<br>
                                The Qube, C.T.S. No.1498A/2<br>
                                Village Marol, Andheri (East)
                            </div>
                        </td>
                        <td width="15%">
                            
                        </td>
                        <td>
                            <div style="padding-bottom: 10px;">
                                <strong style="text-transform: uppercase;">Bill To</strong>
                            </div>
                            <div>
                                Wolters Kluwer India Pvt. Ltd. <br>
                                A-202, 2nd Floor<br>
                                The Qube, C.T.S. No.1498A/2<br>
                                Village Marol, Andheri (East)
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
       
        <div>
            <table style="table-layout: fixed; width: 100%;">
                <thead>
                    <tr>
                        <th  width="40%" align="left" style="border-top: 1px solid #eee; padding: 5px;">
                            Item / Description
                        </th>
                        <th align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            Qty / Hr
                        </th>
                        <th align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            Unit Price
                        </th>
                        <th align="right" style="border-top: 1px solid #eee; padding: 5px;">
                            Amount
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border-top: 1px solid #eee; padding: 5px;">
                            Lorem ipsum dolor sit amet
                        </td>
                        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            10
                        </td>
                        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            50
                        </td>
                        <td align="right" style="border-top: 1px solid #eee; padding: 5px;">
                            USD 500.00
                        </td>
                    </tr>
                    <tr>
                        <td style="border-top: 1px solid #eee; padding: 5px;">
                            Lorem ipsum dolor sit amet
                        </td>
                        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            10
                        </td>
                        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            50
                        </td>
                        <td align="right" style="border-top: 1px solid #eee; padding: 5px;">
                            USD 500.00
                        </td>
                    </tr>
                    <tr>
                        <td style="border-top: 1px solid #eee; padding: 5px;">
                            Lorem ipsum dolor sit amet
                        </td>
                        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            10
                        </td>
                        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            50
                        </td>
                        <td align="right" style="border-top: 1px solid #eee; padding: 5px;">
                            USD 500.00
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div style="border-top: 1px solid #eee;">
            <table style="table-layout: fixed; width: 100%; border-collapse: collapse;">
                <tbody>
                    <tr>
                        <td align="right" style="padding: 5px;">
                            Subtotal
                        </td>
                        <td align="right" width="20%" style="padding: 5px;">
                            1500.00   
                        </td>
                    </tr>
                    <tr>
                        <td align="right" style="padding: 5px;">
                            + TAX    
                        </td>
                        <td align="right" width="20%" style="padding: 5px;">
                            5.00   
                        </td>
                    </tr>
                    <tr>
                        <td align="right" style="padding: 5px;">
                            - Discount    
                        </td>
                        <td align="right" width="20%" style="padding: 5px;">
                            10.00   
                        </td>
                    </tr>
                    <tr>
                        <td align="right" style="border-top: 2px solid #eee; padding: 8px;">
                            <span style="font-size: 16pt;">
                                Total Amount        
                            </span>
                        </td>
                        <td align="right" width="20%" style="border-top: 2px solid #eee; padding: 8px;">
                            <strong style="font-size: 16pt;">
                                USD 1495.00
                            </strong>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div>
            <div style="padding-top:1cm; padding-bottom: 1cm;">
                <div>
                    <strong>Note</strong>
                </div>
                <p style="font-size: 10pt; line-height: 14pt;">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris eget placerat turpis, in vehicula elit. Pellentesque id pharetra ligula, sit amet interdum erat. Integer id lectus pulvinar, maximus urna quis, accumsan lacus. Etiam ac quam magna. Fusce ex lectus, pretium id commodo sit amet, egestas mattis lectus. Vestibulum id libero fringilla magna tincidunt egestas. Nam lacinia sollicitudin ante sed auctor. Suspendisse potenti.
                </p>
            </div>
        </div>
</body>

</html>


"""
