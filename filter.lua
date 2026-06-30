local output = 'docs/'

function to_filename(s)
    local t = {}
    for w in s:gmatch('[%w%.]+') do
        table.insert(t, w)
    end
    return table.concat(t, '-'):lower()
end

function split_more(header)
    return header.level == 3 and pandoc.utils.stringify(header.content) == 'COMMAND INTERFACE'
end

function Pandoc(doc)
    while doc.blocks[1].tag ~= 'Header' or doc.blocks[1].level < 3 do
        table.remove(doc.blocks, 1)
    end

    local comps
    local split = false
    local id_to_link = {}
    for _, blk in ipairs(doc.blocks) do
        if blk.tag == 'Header' then
            local id = to_filename(pandoc.utils.stringify(blk.content))
            local link = {}
            if blk.level == 3 then
                comps = { id }
                split = split_more(blk)
                if split then
                    table.insert(comps, 'index')
                end
            elseif blk.level == 4 and split then
                comps = { comps[1], id }
            else
                link.hash = id:gsub('%.', '')
            end
            if not id_to_link[id] then
                link.filename = pandoc.path.join(comps)
                id_to_link[id] = link
            end
        end
    end

    local headers = pandoc.List()
    local blks = nil
    local nav = {}
    function submit()
        local comps = { output }
        for _, h in ipairs(headers) do
            table.insert(comps, to_filename(pandoc.utils.stringify(h.content)))
        end
        local header = headers:at(-1)
        if split_more(header) then
            table.insert(comps, 'index')
        elseif header.level == 3 and comps[#comps] == 'description' then
            comps[#comps] = 'index'
        end
        local filename = pandoc.path.join(comps) .. '.md'
        local dirname = pandoc.path.directory(filename)
        local doc = pandoc.Pandoc(blks, doc.meta):walk {
            Link = function(el)
                local m = el.target:match('^#(.+)')
                if m then
                    local link = id_to_link[m]
                    if link then
                        local path = pandoc.path.join({ output, link.filename })
                        local ref = pandoc.path.make_relative(path, dirname, true)
                        if ref ~= comps[#comps] then
                            el.target = ref .. '.md'
                            if link.hash then
                                el.target = el.target .. '#' .. link.hash
                            end
                        end
                    end
                end
                return el
            end
        }
        local markdown = pandoc.write(doc, 'markdown_mmd')

        local title = pandoc.utils.stringify(header.content)
        if header.level == 3 then
            local dict = {
                MACOS = 'macOS',
                WINDOWS = 'Windows',
                JAVASCRIPT = 'JavaScript',
                JSON = 'JSON',
                GUI = 'GUI',
                IPC = 'IPC',
            }
            local first = true
            local words = {}
            for w in title:gmatch('%S+') do
                if first then
                    table.insert(words, dict[w] or w:sub(1, 1):upper() .. w:sub(2):lower())
                    first = false
                else
                    table.insert(words, dict[w] or w:lower())
                end
            end
            title = table.concat(words, ' ')
        end

        pandoc.system.make_directory(dirname, true)
        local file, err = io.open(filename, 'w')
        if err then
            error(err)
        end
        file:write('---\n')
        file:write('title: ' .. title .. '\n')
        file:write('---\n\n')
        file:write(markdown)
        local ok, _, code = file:close()
        if not ok then
            error('exit code ' .. code)
        end

        filename = pandoc.path.make_relative(filename, output)
        comps = pandoc.path.split(filename)
        local cursor = nav
        for i = 1, #comps - 1 do
            if i == #comps - 1 and comps[#comps] == 'index.md' then
                local list = {}
                table.insert(cursor, { [title] = list })
                cursor = list
            else
                cursor = cursor[#cursor]
                for _, v in pairs(cursor) do
                    cursor = v
                    break
                end
            end
        end
        table.insert(cursor, { [title] = filename })
    end

    for _, blk in ipairs(doc.blocks) do
        if blk.tag == 'Header' then
            blk.attr.identifier = ''
        end
        if blk.tag == 'Header' and (blk.level == 3 or (blk.level == 4 and headers:find_if(split_more))) then
            if #headers > 0 then
                submit()
            end
            while #headers > 0 and headers:at(-1).level >= blk.level do
                headers:remove()
            end
            headers:insert(blk)
            blks = {}
        else
            table.insert(blks, blk)
        end
    end
    submit()

    local lines = {}
    for line in io.lines('zensical.toml') do
        table.insert(lines, line)
    end
    local file, err = io.open('zensical.toml', 'w')
    if err then
        error(err)
    end

    function write(items, indent)
        indent = indent or 1
        for _, item in ipairs(items) do
            for title, v in pairs(item) do
                file:write(string.rep('  ', indent))
                file:write('{ "' .. title .. '" = ')
                if type(v) == 'string' then
                    file:write('"' .. v .. '" },\n')
                else
                    file:write('[\n')
                    write(v, indent + 1)
                    file:write(string.rep('  ', indent) .. '] },\n')
                end
                break
            end
        end
    end

    local in_nav = false
    for _, line in ipairs(lines) do
        if in_nav and line == ']' then
            in_nav = false
        end
        if not in_nav then
            file:write(line)
            file:write('\n')
        end
        if line == 'nav = [' then
            in_nav = true
            write(nav)
        end
    end
    local ok, _, code = file:close()
    if not ok then
        error('exit code ' .. code)
    end

    return pandoc.Pandoc({})
end
