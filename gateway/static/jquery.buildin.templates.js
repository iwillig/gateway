/* htmlbuilder/JsonML templates
 * -- uses htmlbuilder and JsonML's syntax to generate arrays that can 
 *    be converted into commonly used HTML structures
 * -- Purpose:
 *    <table><tbody><tr><td>This is so much work!</td></tr></tbody></table>
 * -- original examples include: table
 *
 * Usage:
 *   builder.templates.table(
 *     {<options>}, //<==options are optional
 *     [<th 1 contents>, <th 2 contents>],
 *     [<td 1 contents>, <td 2 contents>]
 *   )
 *
 * Example:
 *       var table = builder.templates.table(['header1','header2'], ['item1', 'item2'])
 *
 * This will give you a buildable array:
 *      ['table', {}, 
 *          ['tbody', {},
 *              ['tr', {},
 *                  ['th', {}, 'header1'],
 *                  ['th', {}, 'header2']
 *              ],
 *              ['tr', {},
 *                  ['td', {}, 'item1'],
 *                  ['td', {}, 'item2']
 *              ]
 *          ]
 *      ]
 *
 * Which you can build and insert!
 *       document.body.appendChild(builder.build(table))
 */
;if(typeof(window.builder)=='undefined'){window.builder={}}

builder.templatesVersion = "0.03";

builder.templates=(function(){
	function TableTemplate(options) {
		var rowCount, val, _currentRow, colIndex,
			_optsPresent = !((options instanceof Array) && (typeof(options)!=='string')),
			opts = _optsPresent ? options : {},
			argCountRowStart = _optsPresent ? 1 : 0, //skips first argument if _optsPresent
			useTHs = (opts.th || true),
			_contents = ["tbody", {}];
		
		for(rowCount = argCountRowStart; rowCount<arguments.length; rowCount++) {
			val=arguments[rowCount];
			_currentRow = ["tr", {}];
			for(colIndex=0; colIndex<val.length; colIndex++) {
				_currentRow.push([
					(useTHs && rowCount==argCountRowStart) ? "th" : "td",
					{},
					val[colIndex]
				]);
			}
			_contents.push(_currentRow);
		}
		return [
			"table", {},
			_contents
		];
	}
	
	return {
		table: TableTemplate
	}
})();